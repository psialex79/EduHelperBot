"""Модуль для обработки ответов учеников."""

import logging
from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from db_operations.student_db_operations import get_right_answer_for_student, get_next_assignment, get_topic_id_by_assignment, get_homework_file_id_by_topic
from states.student_states import StudentActions
from keyboards.student_keyboard import get_hint_inline_kb, get_solution_inline_kb
import text_messages
from student_handlers.assignment_handling import is_photo

router = Router()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.message(StudentActions.waiting_for_answer)
async def process_input_answer(message: Message, state: FSMContext, bot: Bot):
    """Обрабатывает ответ ученика на задание."""
    student_answer = message.text
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    data = await state.get_data()
    current_assignment_id = data.get('current_assignment_id')
    right_answer = get_right_answer_for_student(current_assignment_id)

    if right_answer is None:
        await message.answer(text_messages.ASSIGNMENT_NOT_FOUND)
        return

    if student_answer.lower() == right_answer.lower():
        logger.info(f"Ученик {user_name} (ID: {user_id}) ответил правильно на задание.")
        await handle_correct_answer(message, state, bot, current_assignment_id, user_id)
    else:
        logger.info(f"Ученик {user_name} (ID: {user_id}) ответил неправильно на задание.")
        await handle_incorrect_answer(message, state, data)

async def send_homework_file(bot: Bot, user_id: int, current_assignment_id: str):
    """Отправляет файл для самостоятельной работы, если он есть."""
    topic_id = get_topic_id_by_assignment(current_assignment_id)
    homework_file_id = get_homework_file_id_by_topic(topic_id)

    if homework_file_id:
        if is_photo(homework_file_id):
            await bot.send_photo(user_id, homework_file_id)
        else:
            await bot.send_document(user_id, homework_file_id)
    else:
        await bot.send_message(user_id, text_messages.NO_HOMEWORK_FILE)

async def handle_correct_answer(message, state, bot, current_assignment_id, user_id):
    """Обрабатывает случай правильного ответа ученика."""
    await message.answer(text_messages.CORRECT_ANSWER)
    next_assignment = get_next_assignment(current_assignment_id)
    if next_assignment:
        await state.update_data(
            current_assignment_id=next_assignment['_id'],
            hint_shown=False,
            incorrect_attempts=0
        )
        await bot.send_photo(user_id, next_assignment['task_file'])
        await message.answer(text_messages.ENTER_ANSWER)
        await state.set_state(StudentActions.waiting_for_answer)
    else:
        await message.answer(text_messages.LAST_ASSIGNMENT)
        await send_homework_file(bot, user_id, current_assignment_id)
        await state.clear()

async def handle_incorrect_answer(message, state, data):
    """Обрабатывает случай неправильного ответа ученика."""
    incorrect_attempts = data.get('incorrect_attempts', 0)
    incorrect_attempts += 1

    if incorrect_attempts < 2:
        await message.answer(text_messages.INCORRECT_ANSWER, reply_markup=get_hint_inline_kb())
        await state.update_data(hint_shown=True, incorrect_attempts=incorrect_attempts)
    else:
        await message.answer(text_messages.INCORRECT_ANSWER, reply_markup=get_solution_inline_kb())
        await state.update_data(incorrect_attempts=0)

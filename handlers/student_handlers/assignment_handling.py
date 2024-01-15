"""Модуль для обработки заданий учеников."""

import logging
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
import text_messages
from db_operations.student_db_operations import get_assignments_by_topic, get_next_assignment, get_topic_id_by_assignment, get_homework_file_id_by_topic
from states.student_states import StudentActions

router = Router()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.callback_query(F.data.startswith("assignments_"))
async def send_first_assignment(callback: CallbackQuery, state: FSMContext, bot: Bot):
    try:
        user_id = callback.from_user.id
        topic_id = callback.data.split("_")[1]
        assignments = get_assignments_by_topic(topic_id)
        if assignments:
            first_assignment = assignments[0]
            try:
                logger.info(f"Попытка отправить файл как фото: {first_assignment['task_file']}")
                await bot.send_photo(user_id, first_assignment['task_file'])
            except Exception as e:
                logger.info(f"Отправка файла как фото не удалась, попытка как документ: {first_assignment['task_file']}, ошибка: {e}")
                await bot.send_document(user_id, first_assignment['task_file'])
            await callback.message.answer(text_messages.ENTER_ANSWER)
            await state.set_state(StudentActions.waiting_for_answer)
        else:
            await bot.send_message(user_id, text_messages.NO_ASSIGNMENTS)

    except Exception as e:
        logger.error(f"Произошла ошибка в send_first_assignment: {e}")
        await bot.send_message(user_id, "Произошла ошибка, пожалуйста, попробуйте позже")
    await callback.answer()

@router.callback_query(F.data == "next_assignment")
async def send_next_assignment(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Отправляет следующее задание ученику после правильного ответа на предыдущее."""
    user_name = callback.from_user.full_name
    data = await state.get_data()
    current_assignment_id = data.get('current_assignment_id')
    logger.info(f"Ученик {user_name} запросил следующее задание.")
    if current_assignment_id:
        next_assignment = get_next_assignment(current_assignment_id)
        if next_assignment:
            await bot.send_photo(callback.from_user.id, next_assignment['task_file'])
            await state.update_data(current_assignment_id=next_assignment['_id'])
            await callback.message.answer(text_messages.ENTER_ANSWER)
            await state.set_state(StudentActions.waiting_for_answer)
        else:
            await callback.message.answer(text_messages.LAST_ASSIGNMENT)
            topic_id = get_topic_id_by_assignment(current_assignment_id)
            homework_file_id = get_homework_file_id_by_topic(topic_id)
            if homework_file_id:
                await bot.send_document(callback.from_user.id, homework_file_id)
            else:
                await bot.send_message(callback.from_user.id, text_messages.NO_HOMEWORK_FILE)
    else:
        await callback.message.answer(text_messages.ASSIGNMENT_NOT_FOUND)
    await callback.answer()

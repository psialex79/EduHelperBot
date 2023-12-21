"""Модуль для обработки заданий учеников."""

import logging
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
import text_messages
from db_operations.student_db_operations import get_assignments_by_topic, get_next_assignment
from states.student_states import StudentActions

router = Router()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.callback_query(F.data.startswith("assignments_"))
async def send_first_assignment(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Отправляет первое задание ученику по выбранной теме."""
    user_id = callback.from_user.id
    user_name = callback.from_user.full_name
    topic_id = callback.data.split("_")[1]

    assignments = get_assignments_by_topic(topic_id)
    logger.info(f"Ученик {user_name} (ID: {user_id}) запросил первое задание по теме с ID: {topic_id}")

    if assignments:
        await state.update_data(
            current_assignment_index=0,
            total_assignments=len(assignments),
            current_assignment_id=assignments[0]['_id']
            )
        await bot.send_photo(callback.from_user.id, assignments[0]['task_file'])
        await callback.message.answer(text_messages.ENTER_ANSWER)
        await state.set_state(StudentActions.waiting_for_answer)
    else:
        await bot.send_message(callback.from_user.id, text_messages.NO_ASSIGNMENTS)

    await callback.answer()

@router.callback_query(F.data == "next_assignment")
async def send_next_assignment(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Отправляет следующее задание ученику после правильного ответа на предыдущее."""
    user_id = callback.from_user.id
    user_name = callback.from_user.full_name

    data = await state.get_data()
    current_assignment_id = data.get('current_assignment_id')

    logger.info(f"Ученик {user_name} (ID: {user_id}) запросил следующее задание.")

    if current_assignment_id:
        next_assignment = get_next_assignment(current_assignment_id)

        if next_assignment:
            await bot.send_photo(callback.from_user.id, next_assignment['task_file'])
            await state.update_data(current_assignment_id=next_assignment['_id'])
            await callback.message.answer(text_messages.ENTER_ANSWER)
            await state.set_state(StudentActions.waiting_for_answer)
        else:
            await callback.message.answer(text_messages.LAST_ASSIGNMENT)
            await state.clear()
    else:
        await callback.message.answer(text_messages.ASSIGNMENT_NOT_FOUND)

    await callback.answer()

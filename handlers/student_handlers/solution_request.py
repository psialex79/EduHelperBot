"""Модуль для обработки запросов на получение решения задания в Telegram-боте."""

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from db_operations.student_db_operations import get_latest_assignment_for_student
import text_messages
from keyboards.student_keyboard import get_next_assignment_keyboard

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

@router.callback_query(F.data == "show_solution")
async def cmd_request_solution(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает запрос на получение решения к текущему заданию."""
    data = await state.get_data()
    current_assignment_id = data.get('current_assignment_id')

    if current_assignment_id:
        latest_assignment = get_latest_assignment_for_student(current_assignment_id)
        keyboard = get_next_assignment_keyboard()

        if latest_assignment:
            solution_id = latest_assignment.get('solution_file')
            if solution_id:
                logger.info("Отправка решения задания.")
                await callback.bot.send_photo(chat_id=callback.from_user.id, photo=solution_id, reply_markup=keyboard)
            else:
                logger.info("Решение задания отсутствует.")
                await callback.bot.send_message(chat_id=callback.from_user.id, text=text_messages.NO_SOLUTION_FOR_TASK, reply_markup=keyboard)
        else:
            logger.warning("Задание не найдено.")
            await callback.bot.send_message(chat_id=callback.from_user.id, text=text_messages.ASSIGNMENT_NOT_FOUND)
    else:
        logger.warning("ID текущего задания не найден.")
        await callback.bot.send_message(chat_id=callback.from_user.id, text=text_messages.ASSIGNMENT_NOT_FOUND)
        await state.clear()

    await callback.answer()

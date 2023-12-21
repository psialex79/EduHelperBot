"""Модуль для авторизации и начальной навигации пользователя в Telegram-боте."""

import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from db_operations.auth_db_operations import (
    is_registered_teacher,
    is_registered_student,
    add_to_waiting_list,
    is_in_waiting_list
)
from states import student_states
from keyboards.teacher_keyboard import get_sections_students_inline_kb
from keyboards.student_keyboard import get_section_inline_kb
import text_messages
from db_operations.student_db_operations import get_teacher_id_of_student, get_sections_by_teacher

router = Router()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Обрабатывает команду /start, инициируя процесс авторизации и навигации пользователя."""
    await state.clear()
    user_id = message.from_user.id
    user_name = message.from_user.full_name 

    if is_in_waiting_list(user_id):
        logger.info(f"Пользователь {user_name} (ID: {user_id}) в списке ожидания.")
        await message.answer(text_messages.WAITING_FOR_ADDING)
        return

    if is_registered_teacher(user_id):
        logger.info(f"Преподаватель {user_name} (ID: {user_id}) запустил бота.")
        await message.answer(
            text_messages.CHOOSE_ACTION, reply_markup=get_sections_students_inline_kb()
        )
    elif is_registered_student(user_id):
        teacher_id = get_teacher_id_of_student(user_id)
        if teacher_id is None:
            logger.warning(f"Пользователь {user_name} (ID: {user_id}) не найден в базе как ученик.")
            await message.answer("Произошла ошибка: учитель не найден.")
            return
        logger.info(f"Ученик {user_name} (ID: {user_id}) запустил бота.")
        sections = get_sections_by_teacher(teacher_id)
        keyboard = get_section_inline_kb(sections)
        await state.set_state(student_states.StudentActions.choosing_section)
        await message.answer(text_messages.PRESS_TO_GET_ASSIGNMENT, reply_markup=keyboard)
    else:
        logger.info(f"Новый пользователь (ID: {user_id}) начал использовать бота.")
        add_to_waiting_list(user_id)
        await message.answer(text_messages.ADDED_TO_WAITING_LIST)
        await message.answer(str(user_id))

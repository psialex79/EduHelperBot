"""Модуль для отображения разделов в Telegram-боте."""

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from db_operations.student_db_operations import get_sections_by_teacher
from keyboards.teacher_keyboard import get_section_inline_kb

router = Router()

@router.callback_query(F.data == "view_sections")
async def show_sections(callback: CallbackQuery, bot: Bot):
    """Отображает список разделов, доступных учителю."""
    user_id = callback.from_user.id
    sections = get_sections_by_teacher(user_id)
    keyboard = get_section_inline_kb(sections)
    await bot.send_message(user_id, "Выберите раздел:", reply_markup=keyboard)
    await callback.answer()

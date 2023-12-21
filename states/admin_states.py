"""Модуль, определяющий состояния для административных функций в Telegram-боте."""

from aiogram.filters.state import State, StatesGroup

class AddTeacherState(StatesGroup):
    """Состояния для добавления учителя."""
    waiting_for_teacher_id = State()

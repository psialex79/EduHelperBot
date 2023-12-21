"""Модуль, определяющий состояния для функций студента в Telegram-боте."""

from aiogram.filters.state import State, StatesGroup

class StudentActions(StatesGroup):
    """Состояния для действий студентов."""
    choosing_topic = State()
    waiting_for_answer = State()
    choosing_section = State()

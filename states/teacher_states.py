"""Модуль, определяющий состояния для функций учителя в Telegram-боте."""

from aiogram.filters.state import State, StatesGroup

class TeacherActions(StatesGroup):
    """Состояния для действий учителей."""
    choosing_action = State()

class AddStudentState(StatesGroup):
    """Состояния для добавления ученика."""
    waiting_for_student_id = State()

class AddStudentInfoState(StatesGroup):
    """Состояния для дополнительной информации ученика."""
    waiting_for_real_name = State()

class AddTopicStates(StatesGroup):
    """Состояния для добавления темы."""
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_videolink = State()
    waiting_for_testlink = State()
    waiting_for_task_file = State()
    waiting_for_task_hint = State()
    waiting_for_task_answer = State()
    waiting_for_task_solution = State()
    waiting_for_test_link = State()

class AddSectionStates(StatesGroup):
    """Состояния для добавления раздела."""
    waiting_for_title = State()
    waiting_for_description = State()

class AddSelfStudyStates(StatesGroup):
    waiting_for_self_study_file = State()
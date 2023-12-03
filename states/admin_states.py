from aiogram.filters.state import State, StatesGroup

class AddTeacherState(StatesGroup):
    waiting_for_teacher_id = State()
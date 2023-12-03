from aiogram.filters.state import State, StatesGroup

class StudentActions(StatesGroup):
    waiting_for_answer = State()
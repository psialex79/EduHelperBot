from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_assignment_student_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Добавить задание")
    kb.button(text="Добавить ученика")
    kb.adjust(2) 
    return kb.as_markup(resize_keyboard=True)

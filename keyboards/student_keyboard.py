from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_answer_tip_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Ввести ответ")
    kb.button(text="Подсказка")
    kb.adjust(2) 
    return kb.as_markup(resize_keyboard=True)

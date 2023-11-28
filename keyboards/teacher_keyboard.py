from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

def get_assignment_student_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Добавить задание")
    kb.button(text="Добавить ученика")
    kb.adjust(2) 
    return kb.as_markup(resize_keyboard=True)

def get_assignment_student_inline_kb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(
        text="Добавить задание",
        callback_data="adding_task"
    ))
    ikb.add(InlineKeyboardButton(
        text="Добавить ученика",
        callback_data="adding_student"
    ))
    return ikb.as_markup()


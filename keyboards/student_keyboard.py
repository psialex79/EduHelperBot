from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_assignment_inline_kb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(
        text="Получить задание",
        callback_data="getting_task"
    ))
    return ikb.as_markup()

def get_hint_inline_kb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(
        text="Подсказка",
        callback_data="getting_hint"
    ))
    return ikb.as_markup()

def check_or_hint_inline_kb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(
        text="Проверить ответ",
        callback_data="check_answer"
    ))
    ikb.add(InlineKeyboardButton(
        text="Подсказка",
        callback_data="getting_hint"
    ))
    return ikb.as_markup()
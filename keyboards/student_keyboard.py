from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

def get_assignment_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="К задаче")
    kb.button(text="Мой профиль")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def get_answer_tip_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Ввести ответ")
    kb.button(text="Подсказка")
    kb.adjust(2) 
    return kb.as_markup(resize_keyboard=True)

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
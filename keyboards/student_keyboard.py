"""Модуль для создания клавиатур для учеников в Telegram-боте."""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_section_inline_kb(sections) -> InlineKeyboardMarkup:
    """Создает клавиатуру с разделами для ученика."""
    ikb = InlineKeyboardBuilder()
    for section in sections:
        ikb.row(InlineKeyboardButton(
            text=section['title'],
            callback_data=f"section_{section['_id']}"
        ))
    return ikb.as_markup()

def get_hint_inline_kb() -> InlineKeyboardMarkup:
    """Создает клавиатуру для запроса подсказки к заданию."""
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(
        text="Подсказка",
        callback_data="getting_hint"
    ))
    return ikb.as_markup()

def get_solution_inline_kb() -> InlineKeyboardMarkup:
    """Создает клавиатуру для запроса решения задания."""
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(
        text="Показать решение",
        callback_data="show_solution"
    ))
    return ikb.as_markup()

def get_next_assignment_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру для перехода к следующему заданию."""
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(
        text="Следующее задание",
        callback_data="next_assignment"
    ))
    return ikb.as_markup()

def get_materials_inline_kb(topic_id) -> InlineKeyboardMarkup:
    """Создает клавиатуру для доступа к материалам темы."""
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(
        text="Перейти к материалам",
        callback_data=f"materials_{topic_id}"
    ))
    return ikb.as_markup()

def get_next_video_inline_kb(current_index, total_count, topic_id):
    """Создает клавиатуру для перехода к следующему видео или заданиям темы."""
    ikb = InlineKeyboardBuilder()
    if current_index < total_count - 1:
        ikb.row(InlineKeyboardButton(
            text="Следующее видео",
            callback_data=f"next_video_{topic_id}_{current_index + 1}"
        ))
    else:
        ikb.row(InlineKeyboardButton(
            text="Перейти к заданиям",
            callback_data=f"assignments_{topic_id}"
        ))
    return ikb.as_markup()

def get_topics_inline_kb(topics) -> InlineKeyboardMarkup:
    """Создает клавиатуру со списком тем для выбора."""
    ikb = InlineKeyboardBuilder()
    for topic in topics:
        ikb.row(InlineKeyboardButton(
            text=topic['title'],
            callback_data=f"topic_{topic['_id']}"
        ))
    return ikb.as_markup()

"""Модуль для создания клавиатур для учителей в Telegram-боте."""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_sections_students_inline_kb() -> InlineKeyboardMarkup:
    """Создает клавиатуру для перехода к разделам и списку учеников."""
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(
        text="Разделы",
        callback_data="view_sections"
    ))
    ikb.add(InlineKeyboardButton(
        text="Ученики",
        callback_data="addingstudent"
    ))
    return ikb.as_markup()

def get_section_inline_kb(sections) -> InlineKeyboardMarkup:
    """Создает клавиатуру со списком разделов и опцией добавления нового раздела."""
    ikb = InlineKeyboardBuilder()
    for section in sections:
        ikb.row(InlineKeyboardButton(
            text=section['title'],
            callback_data=f"section_{section['_id']}"
        ))
    ikb.add(InlineKeyboardButton(
        text="Добавить раздел",
        callback_data="adding_section"
    ))
    return ikb.as_markup()

def get_topics_inline_kb() -> InlineKeyboardMarkup:
    """Создает клавиатуру для добавления новой темы."""
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(
        text="Добавить тему",
        callback_data="adding_topic"
    ))
    return ikb.as_markup()

def get_studentslist_addstudent_inline_kb() -> InlineKeyboardMarkup:
    """Создает клавиатуру для просмотра списка учеников и добавления нового ученика."""
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(
        text="Список учеников",
        callback_data="studentslist"
    ))
    ikb.add(InlineKeyboardButton(
        text="Добавить ученика",
        callback_data="addingstudent"
    ))
    return ikb.as_markup()

def get_finish_adding_topic_kb() -> InlineKeyboardMarkup:
    """Создает клавиатуру для перехода к добавлению заданий к теме."""
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(
        text="Перейти к вводу заданий",
        callback_data="add_topic_task_file"
    ))
    return ikb.as_markup()

def get_finish_or_add_more_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру для завершения добавления заданий или добавления еще одного задания."""
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(
        text="Закончить",
        callback_data="finish_adding"
    ))
    ikb.add(InlineKeyboardButton(
        text="Добавить еще задание",
        callback_data="add_more_tasks"
    ))
    return ikb.as_markup()

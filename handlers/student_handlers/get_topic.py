"""Модуль для обработки запросов на показ тем и разделов."""

import logging, text_messages
from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from db_operations.student_db_operations import get_topic_by_id, get_section_by_id, get_topics_by_section_id, is_student
from db_operations.teacher_db_operations import is_teacher
from keyboards.student_keyboard import get_materials_inline_kb, get_next_video_inline_kb, get_topics_inline_kb
from keyboards.teacher_keyboard import get_topics_teacher_inline_kb
from bson import ObjectId 

router = Router()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.callback_query(F.data.startswith("topic_"))
async def show_topic_description(callback: CallbackQuery, bot: Bot):
    """Показывает название выбранной темы."""
    topic_id = callback.data.split("_")[1]
    topic = get_topic_by_id(topic_id)
    if topic:
        message_text = f"Тема: {topic['title']}"
        keyboard = get_materials_inline_kb(topic_id)
        await bot.send_message(callback.from_user.id, message_text, reply_markup=keyboard)
    else:
        await bot.send_message(callback.from_user.id, text_messages.NO_TOPIC_FOUND)
    await callback.answer()

@router.callback_query(F.data.startswith("section_"))
async def show_section_description(callback: CallbackQuery, bot: Bot, state: FSMContext):
    user_id = callback.from_user.id
    user_name = callback.from_user.full_name
    section_id = callback.data.split("_")[1]

    section = get_section_by_id(section_id)

    if section:
        logger.info(f"Пользователь {user_name} выбрал раздел: {section['title']}")

        await state.update_data(section_id=section_id)

        topics = get_topics_by_section_id(section_id)
        message_text = f"Раздел: {section['title']}"

        if is_teacher(user_id):
            keyboard = get_topics_teacher_inline_kb(topics)
        elif is_student(user_id):
            keyboard = get_topics_inline_kb(topics)
        else:
            keyboard = None  # Или какая-то другая логика для неопределенных пользователей

        await bot.send_message(callback.from_user.id, message_text, reply_markup=keyboard)
    else:
        await bot.send_message(callback.from_user.id, text_messages.NO_SECTION_FOUND)
        logger.info(f"Раздел с ID: {section_id} не найден")
    await callback.answer()

@router.callback_query(F.data.startswith("materials_"))
async def send_first_video(callback: CallbackQuery, bot: Bot):
    """Отправляет первое видео из списка материалов по теме."""
    topic_id = callback.data.split("_")[1]
    topic = get_topic_by_id(topic_id)
    if topic and topic.get('videos'):
        video_url = topic['videos'][0]
        keyboard = get_next_video_inline_kb(0, len(topic['videos']), topic_id)
        await bot.send_message(callback.from_user.id, video_url, reply_markup=keyboard)
    else:
        await bot.send_message(callback.from_user.id, text_messages.NO_MATERIALS_FOUND)
    await callback.answer()

@router.callback_query(F.data.startswith("next_video_"))
async def send_next_video(callback: CallbackQuery, bot: Bot):
    """Отправляет следующее видео из списка материалов по теме."""
    parts = callback.data.split("_")
    topic_id = parts[2]
    current_index = int(parts[3])

    try:
        topic = get_topic_by_id(ObjectId(topic_id))
        if topic and topic.get('videos') and current_index < len(topic['videos']):
            video_url = topic['videos'][current_index]
            keyboard = get_next_video_inline_kb(current_index, len(topic['videos']), topic_id)
            await bot.send_message(callback.from_user.id, video_url, reply_markup=keyboard)
        else:
            message = text_messages.NO_MORE_MATERIALS_FOUND
            await bot.send_message(callback.from_user.id, message)
    except:
        await bot.send_message(callback.from_user.id, "Возникла ошибка.")
    await callback.answer()

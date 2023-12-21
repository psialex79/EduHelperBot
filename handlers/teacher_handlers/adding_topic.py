"""Модуль для добавления тем и разделов в Telegram-боте."""

from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from db_operations.auth_db_operations import is_registered_teacher
from db_operations.teacher_db_operations import save_topic_to_db, save_section_to_db
from states.teacher_states import AddTopicStates, AddSectionStates
import text_messages, logging
from keyboards.teacher_keyboard import get_finish_adding_topic_kb, get_topics_inline_kb
from models import Topic, Section

router = Router()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.callback_query(F.data == "adding_section")
async def cmd_add_section(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает запрос на добавление раздела."""
    user_id = callback.from_user.id
    if is_registered_teacher(user_id):
        await state.set_state(AddSectionStates.waiting_for_title)
        await callback.message.answer(text_messages.INPUT_SECTION_NAME)
    else:
        await callback.message.answer(text_messages.COMMAND_FOR_TEACHERS_ONLY)

@router.message(AddSectionStates.waiting_for_title)
async def process_section_title(message: Message, state: FSMContext):
    """Обрабатывает ввод названия раздела и сохраняет раздел."""
    await state.update_data(section_title=message.text)
    section_data = await state.get_data()
    new_section = Section(
        title=section_data["section_title"],
        teacher_id=message.from_user.id
    )
    section_id = save_section_to_db(new_section)
    logger.info(f"Пользователь {message.from_user.full_name} (ID: {message.from_user.id}) добавил новый раздел с ID: {section_id}")
    await state.update_data(section_id=section_id) 
    await message.answer(text_messages.ADD_TOPIC, reply_markup=get_topics_inline_kb())

@router.callback_query(F.data == "adding_topic")
async def cbk_add_topic(callback: CallbackQuery, bot: Bot, state: FSMContext):
    """Обрабатывает запрос на добавление темы."""
    user_id = callback.from_user.id
    if is_registered_teacher(user_id):
        section_data = await state.get_data()
        if "section_id" in section_data:
            await state.update_data(teacher_id=user_id)
            await state.set_state(AddTopicStates.waiting_for_title)
            await bot.send_message(user_id, text=text_messages.INPUT_TOPIC_NAME)
        else:
            await bot.send_message(user_id, text=text_messages.NO_SECTION_ID_FOUND)
    else:
        await bot.send_message(user_id, text=text_messages.COMMAND_FOR_TEACHERS_ONLY)

@router.message(AddTopicStates.waiting_for_title)
async def process_topic_title(message: Message, state: FSMContext):
    """Обрабатывает ввод названия темы."""
    await state.update_data(title=message.text)
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    logger.info(f"Пользователь {user_name} (ID: {user_id}) добавляет тему {message.text}")
    await state.set_state(AddTopicStates.waiting_for_videolink)
    await message.answer(text_messages.INPUT_VIDEO_LINK)

@router.callback_query(F.data == "add_topic_task_file")
async def cbk_add_topic_task_file(callback: CallbackQuery, bot: Bot, state: FSMContext):
    """Обрабатывает сохранение темы и переход к добавлению задачи."""
    topic_data = await state.get_data()
    new_topic = Topic(
        section_id=topic_data["section_id"],
        title=topic_data["title"],
        teacher_id=topic_data["teacher_id"],
        videos=topic_data.get("videos", [])
    )
    topic_id = save_topic_to_db(new_topic)
    user_name = callback.from_user.full_name
    user_id = callback.from_user.id
    logger.info(f"Пользователь {user_name} (ID: {user_id}) завершил добавление темы с ID: {topic_id}")
    await state.update_data(topic_id=topic_id)
    if is_registered_teacher(user_id):
        await state.set_state(AddTopicStates.waiting_for_task_file)
        await bot.send_message(user_id, text=text_messages.TOPIC_ADDED)
    else:
        await bot.send_message(user_id, text=text_messages.COMMAND_FOR_TEACHERS_ONLY)

@router.message(AddTopicStates.waiting_for_videolink)
async def process_videolink(message: Message, state: FSMContext):
    """Обрабатывает ввод ссылок на видео для темы."""
    videolink = message.text
    current_data = await state.get_data()
    videos = current_data.get('videos', [])
    videos.append(videolink)
    await state.update_data(videos=videos)
    await message.answer(text_messages.ADD_ANOTHER_VIDEO, reply_markup=get_finish_adding_topic_kb())

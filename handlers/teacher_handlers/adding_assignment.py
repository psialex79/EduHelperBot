"""Модуль для добавления заданий в Telegram-боте."""

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.fsm.context import FSMContext
from db_operations.teacher_db_operations import save_assignment_to_db, save_homework_to_db
from db_operations.student_db_operations import get_sections_by_teacher
from models import Assignment, Homework
from states.teacher_states import AddTopicStates, AddSelfStudyStates
from keyboards.teacher_keyboard import get_section_inline_kb, get_finish_or_add_more_keyboard, get_self_study_file_confirmation_keyboard
import text_messages

router = Router()

@router.message(AddTopicStates.waiting_for_task_file)
async def process_task_file(message: Message, state: FSMContext):
    """Обрабатывает загрузку файла задания."""
    if message.content_type == ContentType.DOCUMENT:
        file_id = message.document.file_id
    elif message.content_type == ContentType.PHOTO:
        file_id = message.photo[-1].file_id
    else:
        await message.answer(text_messages.SEND_TASK_FILE)
        return
    await state.update_data(task_file=file_id)
    await state.set_state(AddTopicStates.waiting_for_task_hint)
    await message.answer(text_messages.ENTER_HINT)

@router.message(AddTopicStates.waiting_for_task_hint)
async def process_task_hint(message: Message, state: FSMContext):
    """Обрабатывает ввод подсказки для задания."""
    hint = message.text
    await state.update_data(hint=hint)
    await state.set_state(AddTopicStates.waiting_for_task_answer)
    await message.answer(text_messages.INPUT_ANSWER)

@router.message(AddTopicStates.waiting_for_task_answer)
async def process_task_answer(message: Message, state: FSMContext):
    """Обрабатывает ввод ответа на задание."""
    answer_text = message.text
    await state.update_data(answer_text=answer_text)
    await state.set_state(AddTopicStates.waiting_for_task_solution)
    await message.answer(text_messages.INPUT_SOLUTION_FILE)

@router.message(AddTopicStates.waiting_for_task_solution)
async def process_task_solution(message: Message, state: FSMContext):
    """Обрабатывает загрузку файла с решением задания."""
    if message.content_type in [ContentType.PHOTO, ContentType.DOCUMENT]:
        solution_file_id = message.document.file_id if message.document else message.photo[-1].file_id
        await state.update_data(solution_file_id=solution_file_id)
        task_data = await state.get_data()
        new_assignment = Assignment(
            topic_id=task_data['topic_id'],
            task_file=task_data['task_file'],
            hint=task_data.get('hint'),
            answer_text=task_data['answer_text'],
            solution_file=solution_file_id
        )
        save_assignment_to_db(new_assignment) 
        await message.answer("Задание успешно добавлено", reply_markup=get_finish_or_add_more_keyboard())
    else:
        await message.answer("Пожалуйста, отправьте файл с решением")

@router.callback_query(F.data == "add_more_tasks")
async def add_more_tasks(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Обрабатывает добавление дополнительных заданий."""
    await state.set_state(AddTopicStates.waiting_for_task_file)
    await bot.send_message(callback.from_user.id, text="Загрузите файл с заданием")

@router.callback_query(F.data == "finish_adding")
async def finish_adding(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Запрашивает у учителя добавление файла для самостоятельной работы."""
    await callback.message.answer(text_messages.ASK_ADD_SELF_STUDY_FILE, reply_markup=get_self_study_file_confirmation_keyboard())

@router.callback_query(F.data == "add_self_study_file_yes")
async def add_self_study_file_yes(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Обработка согласия на добавление файла."""
    await state.set_state(AddSelfStudyStates.waiting_for_self_study_file)
    await callback.message.answer(text_messages.ADD_SELF_STUDY_FILE)

@router.message(AddSelfStudyStates.waiting_for_self_study_file)
async def process_self_study_file(message: Message, state: FSMContext):
    """Обрабатывает загрузку файла для самостоятельной работы."""
    if message.content_type == ContentType.DOCUMENT:
        file_id = message.document.file_id
        data = await state.get_data()
        topic_id = data.get('topic_id')
        homework = Homework(topic_id, file_id)
        save_homework_to_db(homework)
        await message.answer(text_messages.HOMEWORK_SAVED)
    else:
        await message.answer(text_messages.SEND_DOCUMENT)

@router.callback_query(F.data == "add_self_study_file_no")
async def add_self_study_file_no(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Обработка отказа от добавления файла."""
    sections = get_sections_by_teacher(callback.from_user.id)
    await state.clear()
    await bot.send_message(callback.from_user.id, text_messages.CHOOSE_ACTION, reply_markup=get_section_inline_kb(sections))
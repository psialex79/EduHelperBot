"""Модуль для добавления учеников в Telegram-боте."""

from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from db_operations.auth_db_operations import is_registered_teacher, remove_from_waiting_list, is_in_waiting_list
from db_operations.teacher_db_operations import add_student 
from states import teacher_states
import text_messages, logging

router = Router()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.callback_query(F.data == "addingstudent")
async def cmd_add_student(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает запрос на добавление ученика."""
    teacher_name = callback.from_user.full_name
    teacher_id = callback.from_user.id

    logger.info(f"Преподаватель {teacher_name} начал процесс добавления ученика")

    if is_registered_teacher(teacher_id):
        await callback.message.answer(text_messages.ENTER_STUDENT_ID)
        await state.set_state(teacher_states.AddStudentState.waiting_for_student_id)
    else:
        await callback.message.answer(text_messages.COMMAND_FOR_TEACHERS_ONLY)

@router.message(teacher_states.AddStudentState.waiting_for_student_id)
async def process_student_id(message: Message, state: FSMContext):
    """Обрабатывает ввод ID ученика."""
    if message.text.lower() == "отмена":
        await state.clear()
        await message.answer(text_messages.STUDENT_ADDING_CANCEL)
        return

    try:
        student_id = int(message.text)
    except ValueError:
        await message.answer(text_messages.INCORRECT_STUDENT_ID)
        return 
    teacher_id = message.from_user.id
    teacher_name = message.from_user.full_name

    logger.info(f"Преподаватель {teacher_name} ввел ID ученика: {student_id}")

    if is_in_waiting_list(student_id):
        remove_from_waiting_list(student_id)
        await state.set_state(teacher_states.AddStudentInfoState.waiting_for_real_name)
        await state.update_data(student_id=student_id, teacher_id=teacher_id)
        await message.answer(text_messages.ENTER_REAL_NAME, reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(text_messages.INCORRECT_STUDENT_ID)

@router.message(teacher_states.AddStudentInfoState.waiting_for_real_name)
async def process_real_name(message: Message, state: FSMContext, bot: Bot):
    """Обрабатывает ввод реального имени ученика и добавляет ученика в систему."""
    if message.text.lower() == "отмена":
        await state.clear()
        await message.answer(text_messages.STUDENT_ADDING_CANCEL)
        return
    
    real_name = message.text
    user_data = await state.get_data()
    student_id = user_data['student_id']
    teacher_id = user_data['teacher_id']
    teacher_name = message.from_user.full_name

    logger.info(f"Преподаватель {teacher_name} (ID: {teacher_id}) добавил ученика с ID {student_id} и именем '{real_name}'")

    add_student(student_id, real_name, teacher_id)
    await bot.send_message(student_id, text_messages.STUDENT_NOTIFICATION_ADDED.format(real_name))
    await message.answer(text_messages.STUDENT_ADDED.format(student_id, real_name))
    await state.set_state(teacher_states.TeacherActions.choosing_action)

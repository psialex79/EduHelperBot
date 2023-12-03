from aiogram import Router, F, Bot
from aiogram.types import Message, ContentType, CallbackQuery
from aiogram.fsm.context import FSMContext

from db_operations.auth_db_operations import is_registered_teacher
from db_operations.teacher_db_operations import add_assignment, get_students_of_teacher
from states import teacher_states
import text_messages

router = Router()

@router.callback_query(F.data == "adding_task")
async def cmd_add_assignment(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_id = callback.from_user.id
    if is_registered_teacher(user_id):
        await state.set_state(teacher_states.AddAssignmentState.waiting_for_file)
        await bot.send_message(user_id, text=text_messages.SEND_ASSIGNMENT_FILE)
    else:
        await bot.send_message(user_id, text=text_messages.COMMAND_FOR_TEACHERS_ONLY)

@router.message(teacher_states.AddAssignmentState.waiting_for_file)
async def process_assignment_file(message: Message, state: FSMContext):
    is_photo = False
    if message.content_type == ContentType.PHOTO:
        file_id = message.photo[-1].file_id
        is_photo = True
    elif message.content_type == ContentType.DOCUMENT:
        file_id = message.document.file_id

    teacher_id = message.from_user.id
    await state.update_data(file_id=file_id, teacher_id=teacher_id, is_photo=is_photo)
    await state.set_state(teacher_states.AddAssignmentState.waiting_for_right_answer)
    await message.answer(text_messages.ASSIGNMENT_UPLOADED)

@router.message(teacher_states.AddAssignmentState.waiting_for_right_answer)
async def process_right_answer(message: Message, state: FSMContext):
    right_answer = message.text
    await state.update_data(right_answer=right_answer)
    await state.set_state(teacher_states.AddAssignmentState.waiting_for_hint)
    await message.answer(text_messages.LOAD_HINT_OR_SKIP)

@router.message(teacher_states.AddAssignmentState.waiting_for_hint)
async def process_hint(message: Message, state: FSMContext, bot: Bot):
    hint = None
    if message.text != '/skip':
        if message.content_type == ContentType.TEXT:
            hint = message.text
        elif message.content_type in [ContentType.PHOTO, ContentType.DOCUMENT]:
            hint = message.photo[-1].file_id if message.content_type == ContentType.PHOTO else message.document.file_id

    user_data = await state.get_data()
    file_id = user_data['file_id']
    teacher_id = user_data['teacher_id']
    is_photo = user_data['is_photo']
    right_answer = user_data['right_answer']
    add_assignment(teacher_id, file_id, right_answer, hint, is_photo, bot)
    await message.answer(text_messages.CORRECT_ANSWER_SAVED)
    
    student_ids = get_students_of_teacher(teacher_id)
    for student_id in student_ids:
        await bot.send_message(student_id, text_messages.NEW_ASSIGNMENT_NOTIFICATION)
   
    await state.clear()
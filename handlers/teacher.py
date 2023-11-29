from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove, ContentType, CallbackQuery
from aiogram.fsm.context import FSMContext

from db_handlers.auth_handlers import is_registered_teacher, remove_from_waiting_list, is_in_waiting_list
from db_handlers.teacher_handlers import add_student, add_assignment, get_students_of_teacher
from states import AddStudentState, AddStudentInfoState, TeacherActions, AddAssignmentState
import text_messages

router = Router()

@router.callback_query(F.data == "adding_student")
async def cmd_add_student(callback: CallbackQuery, state: FSMContext):
    if is_registered_teacher(callback.from_user.id):
        await callback.answer(text_messages.ENTER_STUDENT_ID)
        await state.set_state(AddStudentState.waiting_for_student_id)
    else:
        await callback.answer(text_messages.COMMAND_FOR_TEACHERS_ONLY)

@router.message(AddStudentState.waiting_for_student_id)
async def process_student_id(message: Message, state: FSMContext):
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

    if is_in_waiting_list(student_id):
        remove_from_waiting_list(student_id)
        await state.set_state(AddStudentInfoState.waiting_for_real_name)
        await state.update_data(student_id=student_id, teacher_id=teacher_id)
        await message.answer(text_messages.ENTER_REAL_NAME, reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(text_messages.INCORRECT_STUDENT_ID)

@router.message(AddStudentInfoState.waiting_for_real_name)
async def process_real_name(message: Message, state: FSMContext, bot: Bot):
    real_name = message.text
    user_data = await state.get_data()
    student_id = user_data['student_id']
    teacher_id = user_data['teacher_id']

    add_student(student_id, real_name, teacher_id)
    await bot.send_message(student_id, text_messages.STUDENT_NOTIFICATION_ADDED.format(real_name))
    await message.answer(text_messages.STUDENT_ADDED.format(student_id, real_name))
    await state.set_state(TeacherActions.choosing_action)


@router.callback_query(F.data == "adding_task")
async def cmd_add_assignment(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_id = callback.from_user.id
    if is_registered_teacher(user_id):
        await state.set_state(AddAssignmentState.waiting_for_file)
        await bot.send_message(user_id, text=text_messages.SEND_ASSIGNMENT_FILE)
    else:
        await bot.send_message(user_id, text=text_messages.COMMAND_FOR_TEACHERS_ONLY)

@router.message(AddAssignmentState.waiting_for_file)
async def process_assignment_file(message: Message, state: FSMContext):
    is_photo = False
    if message.content_type == ContentType.PHOTO:
        file_id = message.photo[-1].file_id
        is_photo = True
    elif message.content_type == ContentType.DOCUMENT:
        file_id = message.document.file_id

    teacher_id = message.from_user.id
    await state.update_data(file_id=file_id, teacher_id=teacher_id, is_photo=is_photo)
    await state.set_state(AddAssignmentState.waiting_for_right_answer)
    await message.answer(text_messages.ASSIGNMENT_UPLOADED)

@router.message(AddAssignmentState.waiting_for_right_answer)
async def process_right_answer(message: Message, state: FSMContext):
    right_answer = message.text
    await state.update_data(right_answer=right_answer)
    await state.set_state(AddAssignmentState.waiting_for_hint)
    await message.answer(text_messages.LOAD_HINT_OR_SKIP)

@router.message(AddAssignmentState.waiting_for_hint)
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



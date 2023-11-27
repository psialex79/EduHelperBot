from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove, ContentType
from aiogram.fsm.context import FSMContext

from db_handlers.auth_handlers import is_registered_teacher, remove_from_waiting_list, is_in_waiting_list
from db_handlers.teacher_handlers import add_student, add_assignment, get_students_of_teacher
from states import AddStudentState, AddStudentInfoState, TeacherActions, AddAssignmentState
import text_messages

router = Router()

@router.message(F.text.lower() == "добавить ученика")
async def cmd_add_student(message: Message, state: FSMContext):
    if is_registered_teacher(message.from_user.id):
        await state.set_state(AddStudentState.waiting_for_student_id)
        await message.answer(text_messages.ENTER_STUDENT_ID)
    else:
        await message.answer(text_messages.COMMAND_FOR_TEACHERS_ONLY)

@router.message(AddStudentState.waiting_for_student_id)
async def process_student_id(message: Message, state: FSMContext):
    try:
        student_id = int(message.text)
        teacher_id = message.from_user.id

        if is_in_waiting_list(student_id):
            remove_from_waiting_list(student_id)

        await state.set_state(AddStudentInfoState.waiting_for_real_name)
        await state.update_data(student_id=student_id, teacher_id=teacher_id)
        await message.answer(text_messages.ENTER_REAL_NAME, reply_markup=ReplyKeyboardRemove())
    except ValueError:
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


@router.message(F.text.lower() == "добавить задание")
async def cmd_add_assignment(message: Message, state: FSMContext):
    if is_registered_teacher(message.from_user.id):
        await state.set_state(AddAssignmentState.waiting_for_file)
        await message.answer(text_messages.SEND_ASSIGNMENT_FILE)
    else:
        await message.answer(text_messages.COMMAND_FOR_TEACHERS_ONLY)

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
async def process_right_answer(message: Message, state: FSMContext, bot: Bot):
    right_answer = message.text
    user_data = await state.get_data()
    file_id = user_data['file_id']
    teacher_id = user_data['teacher_id']
    is_photo = user_data['is_photo']

    add_assignment(teacher_id, file_id, right_answer, is_photo)
    await message.answer(text_messages.CORRECT_ANSWER_SAVED)

    # Получение списка учеников
    student_ids = get_students_of_teacher(teacher_id)

    # Асинхронная отправка сообщения каждому ученику
    for student_id in student_ids:
        await bot.send_message(student_id, "Новое задание добавлено!")

    await state.clear()


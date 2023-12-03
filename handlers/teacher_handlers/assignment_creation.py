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
    teacher_id = message.from_user.id
    file_id = message.document.file_id if message.document else message.photo[-1].file_id
    is_photo = message.content_type == ContentType.PHOTO
    await state.update_data(teacher_id=teacher_id, file_id=file_id, is_photo=is_photo)
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
        else:
            await message.answer(text_messages.HINT_MUST_BE_TEXT)
            return

    await state.update_data(hint=hint)
    await state.set_state(teacher_states.AddAssignmentState.waiting_for_solution_file)
    await message.answer(text_messages.SEND_SOLUTION_FILE)

@router.message(teacher_states.AddAssignmentState.waiting_for_solution_file)
async def process_solution_file(message: Message, state: FSMContext, bot: Bot):
    if message.content_type in [ContentType.PHOTO, ContentType.DOCUMENT]:
        solution_file_id = message.document.file_id if message.document else message.photo[-1].file_id
        await state.update_data(solution_id=solution_file_id)

        user_data = await state.get_data()

        student_ids = add_assignment(user_data['teacher_id'], user_data['file_id'], user_data['right_answer'], user_data.get('hint'), user_data['solution_id'], user_data['is_photo'])

        await message.answer(text_messages.CORRECT_ANSWER_SAVED)
        
        for student_id in student_ids:
            await bot.send_message(student_id, text_messages.NEW_ASSIGNMENT_NOTIFICATION)
       
        await state.clear()
    else:
        await message.answer(text_messages.INVALID_SOLUTION_FILE)

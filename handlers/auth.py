from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from db_handlers.auth_handlers import is_registered_teacher, is_registered_student, add_to_waiting_list, is_in_waiting_list
from db_handlers.student_handlers import get_latest_assignment_for_student
from states import TeacherActions, StudentActions
from keyboards.teacher_keyboard import get_assignment_student_kb
import text_messages

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id

    if is_registered_teacher(user_id):
        await state.set_state(TeacherActions.choosing_action)
        await message.answer(text_messages.CHOOSE_ACTION, reply_markup=get_assignment_student_kb())
    
    elif is_registered_student(user_id):
        latest_assignment = get_latest_assignment_for_student(user_id)
        if latest_assignment:
            file_id = latest_assignment['file_id']
            caption = text_messages.LATEST_ASSIGNMENT_PHOTO_CAPTION if latest_assignment.get('is_photo', False) else text_messages.LATEST_ASSIGNMENT_DOC_CAPTION
            await message.answer_photo(photo=file_id, caption=caption) if latest_assignment.get('is_photo', False) else await message.answer_document(document=file_id, caption=caption)
            await state.set_state(StudentActions.waiting_for_answer)
            await message.answer(text_messages.ENTER_ANSWER)
        else:
            await message.answer(text_messages.NO_ASSIGNMENTS)
    
    else:
        add_to_waiting_list(user_id)
        await message.answer(text_messages.ADDED_TO_WAITING_LIST)
        await message.answer(str(user_id))


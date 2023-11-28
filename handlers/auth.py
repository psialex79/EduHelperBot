from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from db_handlers.auth_handlers import is_registered_teacher, is_registered_student, add_to_waiting_list, is_in_waiting_list
from states import TeacherActions, StudentActions
from keyboards.teacher_keyboard import get_assignment_student_inline_kb
from keyboards.student_keyboard import get_assignment_kb
import text_messages

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id

    if is_in_waiting_list(user_id):
        await message.answer(text_messages.WAITING_FOR_ADDING)
        return

    if is_registered_teacher(user_id):
        await message.answer(text_messages.CHOOSE_ACTION, reply_markup=get_assignment_student_inline_kb())
    
    elif is_registered_student(user_id):
        await state.set_state(StudentActions.waiting_for_answer)
        await message.answer(text_messages.PRESS_TO_GET_ASSIGNMENT, reply_markup=get_assignment_kb())
    
    else:
        add_to_waiting_list(user_id)
        await message.answer(text_messages.ADDED_TO_WAITING_LIST)
        await message.answer(str(user_id))



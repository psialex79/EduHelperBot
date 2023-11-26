from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from db_handlers.admin_handlers import add_teacher
from db_handlers.auth_handlers import remove_from_waiting_list
from states import AddTeacherState
import text_messages

ADMIN_USER_ID = 135002839

router = Router()

@router.message(Command("addteacher"))
async def cmd_add_teacher(message: Message, state: FSMContext):
    if message.from_user.id == ADMIN_USER_ID:
        await state.set_state(AddTeacherState.waiting_for_teacher_id)
        await message.answer(text_messages.ENTER_TEACHER_ID)
    else:
        await message.answer(text_messages.NO_ACCESS)

@router.message(AddTeacherState.waiting_for_teacher_id)
async def process_teacher_id(message: Message, state: FSMContext):
    try:
        teacher_id = int(message.text)
        add_teacher(teacher_id)  
        remove_from_waiting_list(teacher_id)  
        await message.answer(text_messages.TEACHER_ADDED.format(teacher_id))
        await state.clear() 
    except ValueError:
        await message.answer(text_messages.INVALID_TEACHER_ID)
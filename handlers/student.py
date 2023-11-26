from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from db_handlers.student_handlers import get_right_answer_for_student
from states import StudentActions
import text_messages

router = Router()

@router.message(StudentActions.waiting_for_answer)
async def process_student_answer(message: Message, state: FSMContext):
    student_answer = message.text
    user_id = message.from_user.id

    right_answer = get_right_answer_for_student(user_id)
    if right_answer is not None:
        if student_answer.lower() == right_answer.lower():
            await message.answer(text_messages.CORRECT_ANSWER)
            await state.clear()
        else:
            await message.answer(text_messages.INCORRECT_ANSWER)
    else:
        await message.answer(text_messages.ASSIGNMENT_NOT_FOUND)
        await state.clear()


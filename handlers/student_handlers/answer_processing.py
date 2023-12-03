import re
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from db_operations.student_db_operations import get_right_answer_for_student
from states import student_states
from keyboards.student_keyboard import get_hint_inline_kb
import text_messages

router = Router()

@router.message(student_states.StudentActions.waiting_for_answer)
async def process_input_answer(message: Message, state: FSMContext):
    if re.match(r'/', message.text):
        await state.clear()
        return
    
    student_answer = message.text
    user_id = message.from_user.id

    right_answer = get_right_answer_for_student(user_id)
    if right_answer is not None:
        if student_answer.lower() == right_answer.lower():
            await message.answer(text_messages.CORRECT_ANSWER)
            await state.clear()
        else:
            data = await state.get_data()
            hint_shown = data.get('hint_shown', False)

            if not hint_shown:
                await message.answer(text_messages.INCORRECT_ANSWER, reply_markup=get_hint_inline_kb())
                await state.update_data(hint_shown=True)
            else:
                await message.answer(text_messages.INCORRECT_ANSWER)
    else:
        await message.answer(text_messages.ASSIGNMENT_NOT_FOUND)
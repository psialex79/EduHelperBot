from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from db_operations.student_db_operations import get_latest_assignment_for_student
import text_messages

router = Router()

@router.callback_query(F.data == "show_solution")
async def cmd_request_solution(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_id = callback.from_user.id
    latest_assignment = get_latest_assignment_for_student(user_id)

    if latest_assignment and latest_assignment.get('solution_id'):
        solution_id = latest_assignment['solution_id']
        is_solution_photo = latest_assignment.get('is_photo', False)

        if is_solution_photo:
            await callback.bot.send_photo(chat_id=callback.from_user.id, photo=solution_id)
        else:
            await callback.bot.send_document(chat_id=callback.from_user.id, document=solution_id)
    else:
        await callback.bot.send_message(chat_id=callback.from_user.id, text=text_messages.NO_SOLUTION_FOR_TASK)
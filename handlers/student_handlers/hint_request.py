from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from db_operations.student_db_operations import get_latest_assignment_for_student
import text_messages

router = Router()

@router.callback_query(F.data == "getting_hint")
async def cmd_request_tip(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_id = callback.from_user.id
    latest_assignment = get_latest_assignment_for_student(user_id)

    if latest_assignment and latest_assignment.get('hint'):
        hint = latest_assignment['hint']
        await callback.bot.send_message(chat_id=callback.from_user.id, text=text_messages.GETTING_HINT.format(hint))
    else:
        await callback.bot.send_message(chat_id=callback.from_user.id, text=text_messages.NO_HINT_FOR_TASK)
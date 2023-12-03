from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from db_operations.student_db_operations import get_latest_assignment_for_student
import text_messages
from aiogram.exceptions import TelegramAPIError
from states import student_states

router = Router()

@router.callback_query(F.data == "getting_task")
async def cmd_get_assignment(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_id = callback.from_user.id
    latest_assignment = get_latest_assignment_for_student(user_id)
    if latest_assignment:
        file_id = latest_assignment['file_id']
        is_photo = latest_assignment.get('is_photo', False)
        caption = text_messages.LATEST_ASSIGNMENT_PHOTO_CAPTION if is_photo else text_messages.LATEST_ASSIGNMENT_DOC_CAPTION

        try:
            if is_photo:
                await callback.bot.send_photo(chat_id=callback.from_user.id, photo=file_id, caption=caption)
            else:
                await callback.bot.send_document(chat_id=callback.from_user.id, document=file_id, caption=caption)
        except TelegramAPIError as e:
            await callback.bot.send_message(chat_id=callback.from_user.id, text=str(e))

        await callback.message.answer(text_messages.ENTER_ANSWER)
        await state.set_state(student_states.StudentActions.waiting_for_answer)
    else:
        await callback.message.answer(text_messages.NO_ASSIGNMENTS)


import re
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from db_handlers.student_handlers import get_right_answer_for_student, get_latest_assignment_for_student
from states import StudentActions
from keyboards.student_keyboard import get_answer_tip_kb, get_hint_inline_kb
import text_messages

router = Router()

@router.message(StudentActions.waiting_for_answer)
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
            await message.answer(text_messages.INCORRECT_ANSWER, reply_markup=get_hint_inline_kb())
    else:
        await message.answer(text_messages.ASSIGNMENT_NOT_FOUND)
        await state.clear()

@router.callback_query(F.data == "getting_task")
async def cmd_get_assignment(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_id = callback.from_user.id
    latest_assignment = get_latest_assignment_for_student(user_id)
    if latest_assignment:
        file_id = latest_assignment['file_id']
        is_photo = latest_assignment.get('is_photo', False)
        caption = text_messages.LATEST_ASSIGNMENT_PHOTO_CAPTION if is_photo else text_messages.LATEST_ASSIGNMENT_DOC_CAPTION

        if is_photo:
            await callback.bot.send_photo(chat_id=callback.from_user.id, photo=file_id, caption=caption)
        else:
            await callback.bot.send_document(chat_id=callback.from_user.id, document=file_id, caption=caption)

        await callback.answer(text_messages.ENTER_ANSWER, reply_markup=get_answer_tip_kb())
    else:
        await callback.answer(text_messages.NO_ASSIGNMENTS)

@router.callback_query(F.data == "getting_hint")
async def cmd_request_tip(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_id = callback.from_user.id
    latest_assignment = get_latest_assignment_for_student(user_id)

    if latest_assignment and latest_assignment.get('hint'):
        hint = latest_assignment['hint']

        if isinstance(hint, str):
            if hint.startswith('file_id:'):  # Проверяем, является ли подсказка файлом
                file_id = hint.split(':')[1]
                # Определите, является ли файл фотографией или документом, и отправьте его
                # Пример отправки фотографии:
                await callback.bot.send_photo(chat_id=callback.from_user.id, photo=file_id)
                # Для документа используйте:
                # await message.answer_document(document=file_id)
            else:
                # Отправляем текстовую подсказку
                await callback.bot.send_message(chat_id=callback.from_user.id, text=f"Подсказка для задания: {hint}")
        else:
            # Обработка других типов подсказок, если они возможны
            pass
    else:
        await callback.bot.send_message(chat_id=callback.from_user.id, text="Для данного задания подсказка отсутствует.")
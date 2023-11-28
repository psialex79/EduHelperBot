import re
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from db_handlers.student_handlers import get_right_answer_for_student, get_latest_assignment_for_student
from states import StudentKeyboardActions
from keyboards.student_keyboard import get_answer_tip_kb
import text_messages

router = Router()

@router.message(StudentKeyboardActions.waiting_for_answer_input)
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
            await message.answer(text_messages.INCORRECT_ANSWER)
            # Отправляем клавиатуру с выбором действий вместо установки состояния
            await message.answer("Выберите следующее действие:", reply_markup=get_answer_tip_kb())
    else:
        await message.answer(text_messages.ASSIGNMENT_NOT_FOUND)
        await state.clear()

@router.message(F.text.lower() == "к задаче")
async def cmd_get_assignment(message: Message, state: FSMContext):
    user_id = message.from_user.id
    latest_assignment = get_latest_assignment_for_student(user_id)
    if latest_assignment:
        file_id = latest_assignment['file_id']
        is_photo = latest_assignment.get('is_photo', False)
        caption = text_messages.LATEST_ASSIGNMENT_PHOTO_CAPTION if is_photo else text_messages.LATEST_ASSIGNMENT_DOC_CAPTION

        if is_photo:
            await message.answer_photo(photo=file_id, caption=caption)
        else:
            await message.answer_document(document=file_id, caption=caption)

        await message.answer(text_messages.ENTER_ANSWER, reply_markup=get_answer_tip_kb())
    else:
        await message.answer(text_messages.NO_ASSIGNMENTS)

@router.message(F.text.lower() == "ввести ответ")
async def cmd_input_answer(message: Message, state: FSMContext):
    await state.set_state(StudentKeyboardActions.waiting_for_answer_input)
    await message.answer("Введите ваш ответ:")

@router.message(F.text.lower() == "подсказка")
async def cmd_request_tip(message: Message, state: FSMContext):
    user_id = message.from_user.id
    latest_assignment = get_latest_assignment_for_student(user_id)

    if latest_assignment and latest_assignment.get('hint'):
        hint = latest_assignment['hint']

        if isinstance(hint, str):
            if hint.startswith('file_id:'):  # Проверяем, является ли подсказка файлом
                file_id = hint.split(':')[1]
                # Определите, является ли файл фотографией или документом, и отправьте его
                # Пример отправки фотографии:
                await message.answer_photo(photo=file_id)
                # Для документа используйте:
                # await message.answer_document(document=file_id)
            else:
                # Отправляем текстовую подсказку
                await message.answer(f"Подсказка для задания: {hint}")
        else:
            # Обработка других типов подсказок, если они возможны
            pass
    else:
        await message.answer("Для данного задания подсказка отсутствует.")
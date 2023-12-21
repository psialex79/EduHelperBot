"""Модуль, содержащий промежуточное ПО для проверки списка ожидания в Telegram-боте."""

from aiogram import BaseMiddleware
from aiogram.types import Message
from db_operations.auth_db_operations import is_in_waiting_list
import text_messages

class CheckWaitingListMiddleware(BaseMiddleware):
    """Промежуточное ПО, которое проверяет, находится ли пользователь в списке ожидания."""
    async def __call__(self, handler, event, data):
        if isinstance(event, Message):
            user_id = event.from_user.id
            if is_in_waiting_list(user_id):
                await event.answer(text_messages.WAITING_FOR_ADDING)
                return
        return await handler(event, data)

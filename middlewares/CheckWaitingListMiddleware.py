from aiogram import BaseMiddleware
from aiogram.types import Message
from db_handlers.auth_handlers import is_in_waiting_list
import text_messages

class CheckWaitingListMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, Message):
            user_id = event.from_user.id
            if is_in_waiting_list(user_id):
                await event.answer(text_messages.WAITING_FOR_ADDING)
                return
        return await handler(event, data)


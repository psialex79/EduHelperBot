"""Основной модуль для запуска Telegram-бота с использованием aiogram."""
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from middlewares.CheckWaitingListMiddleware import CheckWaitingListMiddleware
from handlers import auth
from handlers.student_handlers import get_student_routers
from handlers.teacher_handlers import get_teacher_routers
from handlers.admin_handlers import get_admin_routers

from config_reader import config

async def main():
    """Основная функция для инициализации и запуска бота."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(config.bot_token.get_secret_value())
    auth_router = auth.router

    for router in get_student_routers():
        router.message.middleware(CheckWaitingListMiddleware())
        dp.include_router(router)

    for router in get_teacher_routers():
        dp.include_router(router)

    for router in get_admin_routers():
        dp.include_router(router)

    dp.include_router(auth_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

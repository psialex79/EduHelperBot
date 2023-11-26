import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import student, teacher, admin, auth
from middlewares.CheckWaitingListMiddleware import CheckWaitingListMiddleware

from config_reader import config

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
        
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(config.bot_token.get_secret_value())

    student_router = student.router
    teacher_router = teacher.router
    admin_router = admin.router
    auth_router = auth.router

    student_router.message.middleware(CheckWaitingListMiddleware())

    dp.include_router(student_router)
    dp.include_router(teacher_router)
    dp.include_router(admin_router)
    dp.include_router(auth_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
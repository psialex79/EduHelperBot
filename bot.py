import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import student, teacher, admin, auth

from config_reader import config

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
        
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(config.bot_token.get_secret_value())

    dp.include_router(student.router)
    dp.include_router(teacher.router)
    dp.include_router(admin.router)
    dp.include_router(auth.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
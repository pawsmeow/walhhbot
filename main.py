
import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database import init_db
from handlers import registration, user_commands, admin_commands

async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    await init_db()

    dp.include_routers(
        registration.router,
        user_commands.router,
        admin_commands.router
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

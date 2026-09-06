from os import getenv
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers.routes import router

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
GROUP_ID = -1004480965680

dp = Dispatcher()
dp.include_router(router)



async def main():
    bot = Bot(token=TOKEN)
    print("🤖 Бот верификации запущен!")

    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types()
    )


if __name__ == "__main__":
    asyncio.run(main())
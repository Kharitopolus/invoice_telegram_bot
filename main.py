import asyncio
from aiogram import Bot, Dispatcher

from base_handlers import router as base_router
from admin.handlers import router as admin_router
from client.handlers import router as client_router
from manager.handlers import router as manager_router
from settings import settings

dp: Dispatcher = Dispatcher()


async def main():
    bot: Bot = Bot(token=settings.bot_token)

    dp.include_router(admin_router)
    dp.include_router(manager_router)
    dp.include_router(client_router)
    dp.include_router(base_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

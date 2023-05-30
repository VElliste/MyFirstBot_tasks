import asyncio
from aiogram import Dispatcher, Bot
from bot import bot
from handlers.start import router as routerStart
from handlers.registration import router as routerRegistration
from handlers.tasks import router as routerTasks
from handlers.editTask import router as routerEditTask
from handlers.unknownMessage import router as routerUnknownMessage
from aiogram.types import  message


async def main():
    dp = Dispatcher()
    dp.include_router(routerStart)
    dp.include_router(routerRegistration)
    dp.include_router(routerTasks)
    dp.include_router(routerEditTask)
    dp.include_router(routerUnknownMessage)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
if __name__ == "__main__":
    asyncio.run(main())

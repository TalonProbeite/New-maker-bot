import asyncio 
from aiogram import Dispatcher, Bot 
from aiogram.types import Message
import logging
from core.seting import settings
from aiogram.filters import Command 
from aiogram import F
from parsers.auxiliary_functions import clear_saved_articles 
from parsers.parser import get_raw_data_aoutomail ,get_raw_data_tarantas
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from generator.generate import get_ready_new
from core.hendlers.hednlers_new import send_new
import random



async def scheduled_clear_articles():
    await clear_saved_articles()
    

async def scheduled_send_new(bot:Bot):
    get_raw_data_tarantas()
    get_ready_new(API=settings.bots.openai_api)
    await send_new(bot=bot)



async def start_bot(bot:Bot):
    # await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, f"Бот запущен, статус: {settings.bots.status}")
    

async def stop_bot(bot:Bot):
    await bot.send_message(settings.bots.admin_id, "Бот остановлен!")

async def start():
    bot = Bot(token=settings.bots.bot_token)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] -  %(name)s - "
                        "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    dp = Dispatcher()

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

    scheduler.add_job(
        scheduled_clear_articles,
        trigger="cron",
        day_of_week="sun",
        hour=0,
        minute=0,
        id="clear_articles"
    )

    scheduler.add_job(
        scheduled_send_new,
        trigger="cron",
        hour="14",
        minute="47",
        id="send_new",
        args=[bot]
    )

    scheduler.start()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    try:
        await dp.start_polling(bot)
    finally:
       await bot.session.close() 
       
  
        


if __name__ == "__main__":
    asyncio.run(start())
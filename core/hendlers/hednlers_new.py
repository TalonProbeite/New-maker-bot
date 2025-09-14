from aiogram import Dispatcher, Bot ,types
from aiogram.types import Message
from core.seting import settings
import json
from aiogram.types import FSInputFile


async def send_new(bot:Bot, path="parsers\data\\new.json"):
    if settings.bots.status == "ON":
        with open(path, "r",encoding="utf-8") as file:
                data = json.load(file)
        image = FSInputFile("parsers\data\\article_arts\\"+data["img"])
        href = data["href"]
        title = data["title"]
        ready_new = data["ready_new"]
        await bot.send_photo(photo=image,caption=f"<a href='{href}'><strong>{title}</strong></a>\n\n{ready_new}", parse_mode="HTML", chat_id= settings.bots.channel_id)
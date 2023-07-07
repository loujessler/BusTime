from aiogram import Bot

from data import config


async def get_bot_link():
    bot = Bot(token=config.API_TOKEN)
    bot_info = await bot.get_me()
    bot_link = f"https://t.me/{bot_info['username']}"
    return bot_link

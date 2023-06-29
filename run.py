import asyncio
from aiogram import executor
from bot.handlers import dp
from bot.loader import shutdown, bot, app
from bot.bot import on_startup

from aiohttp import web

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=shutdown)
from loguru import logger
from aiogram import types
from aiogram.dispatcher.filters import Command

from bot.handlers.main.ttc.search_routes import search_route
from bot.loader import dp
from bot.handlers.main.bot_start import main_menu


@dp.message_handler(commands='search_route')
async def cmd_search_route(message: types.Message):
    print('hello')
    if len(message.get_args()) > 0:  # Если есть аргументы команды
        print(message.get_args())
        await search_route(message, message.get_args())
        # search_route(message.get_args())

from loguru import logger
from aiogram import types
from aiogram.dispatcher.filters import Command

from bot.loader import dp
from bot.handlers.main.bot_start import main_menu


@dp.message_handler(Command('menu'))
async def menu(message: types.Message):
    await message.delete()
    await main_menu(message)
    # LOGS
    logger.log(25, f"The user {message.from_user.id} clicked on /menu button.")

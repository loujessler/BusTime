from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from bot.loader import dp

from bot.handlers.main.settings.settings_menu import handler_settings_menu


@dp.message_handler(Command('settings'))
async def settings_menu_command(message: Message):
    await message.delete()
    await handler_settings_menu(message)

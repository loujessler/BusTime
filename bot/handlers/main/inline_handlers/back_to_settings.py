from aiogram.types import CallbackQuery

from bot.loader import dp
from bot.handlers.main.settings.settings_menu import handler_settings_menu


@dp.callback_query_handler(text='back_to_settings')
async def _back_to_setting(call: CallbackQuery):
    await handler_settings_menu(call)

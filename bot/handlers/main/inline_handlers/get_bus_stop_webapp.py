import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Regexp

from bot.loader import dp, bot

from bot.keyboards.inline.bus_stops import ikb_menu_bus_stops

from bot.states.regist import Regist
from bot.handlers.main.utils.cancel import cancel_func

from bot.utils.db_api import quick_commands as commands
from bot.utils.localization.i18n import MessageFormatter
from bot.handlers.main.utils.my_bus_stops import my_bus_stops

from bot.handlers.main.bot_start import edit_ls


# Отмена при определенных состояниях
@dp.message_handler(content_types=['web_app_data'])
async def get_webapp_data(call: types.CallbackQuery):
    await call.answer(call.message.web_app_data.data)

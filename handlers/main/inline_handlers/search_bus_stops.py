from aiogram import types

from loader import dp, bot

from utils.db_api import quick_commands as commands
from utils.localization.i18n import MessageFormatter


@dp.callback_query_handler(text='search_bus_stops')
async def callback_my_bus_stops(call: types.CallbackQuery):
    user = await commands.select_user(call.from_user.id)
    await bot.answer_callback_query(
        call.id,
        MessageFormatter(user.language).get_message({'send_location': 'none'}),
        show_alert=True
    )

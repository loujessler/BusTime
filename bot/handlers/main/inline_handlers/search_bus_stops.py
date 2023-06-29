from aiogram import types

from bot.loader import dp, bot

from bot.utils.localization.i18n import MessageFormatter


@dp.callback_query_handler(text='search_bus_stops')
async def callback_my_bus_stops(call: types.CallbackQuery):
    user = call.conf.get('user')
    await bot.answer_callback_query(
        call.id,
        MessageFormatter(user.language).get_message({'send_location': 'none'}),
        show_alert=True
    )

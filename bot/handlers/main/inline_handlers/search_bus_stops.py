import asyncio
from aiogram import types
from bot.loader import dp, bot

from bot.keyboards.reply.search_bus_stops_kb import search_stops_kb
from bot.utils.localization.i18n import MessageFormatter


@dp.callback_query_handler(text='search_bus_stops')
async def callback_my_bus_stops(call: types.CallbackQuery):
    user = call.conf.get('user')
    reply_markup = await search_stops_kb(user.language)
    msg_for_del = await call.message.answer(
        text=MessageFormatter(user.language).get_message(format_dict={'search_bus_stops_menu': 'bold',
                                                                      'search_bus_stops_descript': 'none'},
                                                         line_breaks=2),
        reply_markup=reply_markup
    )
    await asyncio.sleep(10)
    await bot.delete_message(call.message.chat.id, msg_for_del.message_id)

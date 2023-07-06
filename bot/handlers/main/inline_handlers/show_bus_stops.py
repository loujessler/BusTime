import asyncio

from aiogram import types
from aiogram.types.web_app_info import WebAppInfo

from bot.handlers.main.utils.page_bus_stops_bld import PageBusStopsBuilder
from bot.loader import dp, bot

from data import config


@dp.callback_query_handler(text='show_bus_stops')
async def callback_show_bus_stops(call: types.CallbackQuery):
    user = call.conf.get('user')
    page_bld = PageBusStopsBuilder(user.language)
    html_name = await page_bld.create_page()
    if config.TEST_WEB_APP:
        route_url = f"https://bustime.ge/test/bus_stops_info/{html_name}"
    else:
        route_url = f"https://bustime.ge/bus_stops_info/{html_name}"
    web_app = WebAppInfo(url=route_url)
    # Create Keyboard
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = types.InlineKeyboardButton(text=f'Открыть карту с остановками',
                                        web_app=web_app)
    keyboard.row(button)
    msg_for_del = await call.message.answer("👇 кнопка с картой остановок", reply_markup=keyboard)
    await asyncio.sleep(10)
    await bot.delete_message(call.message.chat.id, msg_for_del.message_id)

from aiogram import types
from aiogram.types.web_app_info import WebAppInfo

from bot.handlers.main.utils.page_bus_stops_bld import PageBusStopsBuilder
from bot.loader import dp, bot

from bot.utils.localization.i18n import MessageFormatter
from data import config
import time


@dp.callback_query_handler(text='show_bus_stops')
async def callback_show_bus_stops(call: types.CallbackQuery):
    user = call.conf.get('user')
    page_bld = PageBusStopsBuilder(user.language)
    start_time = time.time()
    html_name = await page_bld.create_page()
    end_time = time.time()
    print(f"The function took {end_time - start_time} seconds to complete.")
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
    await call.message.answer("👇 кнопка с картой остановок", reply_markup=keyboard)

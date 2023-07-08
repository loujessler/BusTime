import asyncio
from aiogram import types
from aiogram.types.web_app_info import WebAppInfo

from bot.loader import bot

from bot.handlers.main.utils.page_bus_stops_bld import PageBusStopsBuilder
from bot.utils.localization.i18n import MessageFormatter
from data import config


async def webapp_map_bus_stops(language) -> WebAppInfo:
    page_bld = PageBusStopsBuilder(language)
    html_name = await page_bld.create_page()
    if config.TEST_WEB_APP:
        route_url = f"https://bustime.ge/test/bus_stops_info/{html_name}"
    else:
        route_url = f"https://bustime.ge/bus_stops_info/{html_name}"
    web_app = WebAppInfo(url=route_url)
    return web_app


async def search_stops_kb(language):
    formatter = MessageFormatter(language, 'keyboards')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    web_app = await webapp_map_bus_stops(language)
    button = [
        types.KeyboardButton(text=formatter.get_message({'show_map_bus_stops': 'none'}),
                             web_app=web_app),
        types.KeyboardButton(text=formatter.get_message({'search_nearby_bus_stops': 'none'}),
                             request_location=True)
    ]
    markup.row(*button)
    return markup

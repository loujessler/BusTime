from aiogram.dispatcher.filters import Regexp
from aiogram.types.web_app_info import WebAppInfo

from bot.keyboards.inline.inline_kb_default import ikb_default
from bot.loader import dp, bot
import httpx
from aiogram import types
import folium
import folium.plugins
import os
from transliterate import translit

from bot.utils.additional import capitalize_words
from bot.utils.data_utils.json_data import load_json_data
from data import config


class PageBuilder:
    def __init__(self, route_number: str):
        self.route_number = route_number

    async def check_forwards(self) -> list:
        have_forwards = []
        for forward in [0, 1]:
            data = await load_json_data(f"routes/{self.route_number}_forward_{forward}")

            shape = data['Shape']
            if shape != '':
                have_forwards.append(forward)
        return have_forwards

    async def __get_coord_info(self, forward: str):

        data = await load_json_data(f"routes/{self.route_number}_forward_{forward}")

        shape = data['Shape']

        coordinates = shape.split(",")
        coordinates = [(float(c.split(":")[1]), float(c.split(":")[0])) for c in coordinates]

        stops = data['RouteStops']
        stop_info = [(float(stop['Lat']), float(stop['Lon']), stop['StopId']) for stop in stops]

        return coordinates, stop_info

    async def create_page(self, forward: str) -> str:
        existing_files = os.path.exists(f'data/routes/{self.route_number}_forward_{forward}.html')
        if existing_files and not config.REFRESH_BUS_ROUTES:
            # If file already exists, just send the first match
            html_name = f'{self.route_number}_{forward}.html'
        else:
            # Fetch the route data and generate the map
            coordinates, stop_info = await self.__get_coord_info(forward)

            m = folium.Map(location=coordinates[0], zoom_start=14)
            m.get_root().html.add_child(folium.JavascriptLink('https://telegram.org/js/telegram-web-app.js'))
            folium.plugins.AntPath(coordinates, color="#3d00f7", delay=1000, weight=2.5, opacity=1).add_to(m)

            for stop in stop_info:
                icon = folium.features.CustomIcon('./data/media/bus_stop_icon3.png',
                                                  icon_size=[20, 20])  # Add custom icon
                folium.Marker(location=(stop[0], stop[1]),
                              popup=f"Stop ID: <b>{stop[2]}</b>",
                              icon=icon).add_to(m)
            m.fit_bounds(coordinates)  # Automatically adjust map to show the whole route

            html_name = f"{self.route_number}_forward_{forward}.html"
            m.save(os.path.join('data', 'routes', html_name))

        return html_name


@dp.message_handler(Regexp(r'#\d+$'))
async def command_start(message: types.Message):
    user = message.conf.get('user')
    route_number = message.text[1:]  # Remove the '#' symbol
    await bot.delete_message(message.chat.id, message.message_id)
    if route_number not in await load_json_data('buses_data', 'RouteNumber'):
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Не существует автобуса №{route_number}',
                               parse_mode=types.ParseMode.MARKDOWN)
    else:
        forwards = await PageBuilder(route_number).check_forwards()
        keyboard = types.InlineKeyboardMarkup()
        buttons = []
        for forward in forwards:
            html_name = await PageBuilder(route_number).create_page(forward)
            route_url = f"http://127.0.0.1:8080/data/routes/{html_name}"
            route_url = f"https://bustime.ge/routes/{html_name}"
            web_app = WebAppInfo(url=route_url)
            button = types.InlineKeyboardButton(text=f'{forward}',
                                                web_app=web_app)
            # button = types.InlineKeyboardButton(f'{forward}',
            #                                     callback_data=f'route_{route_number}_{forward}')
            buttons.append(button)
        keyboard.row(*buttons)
        keyboard.inline_keyboard += ikb_default(user.language).inline_keyboard

        await bot.send_message(chat_id=message.chat.id,
                               text=f"Выберете направление:",
                               reply_markup=keyboard)


@dp.callback_query_handler(text_startswith='route_')
async def process_route_bus(call: types.CallbackQuery):
    user = call.conf.get('user')
    # Получаем данные из обратного вызова
    data = call.data.split('_')
    route_number, forward = data[1], data[2]
    html_name = await PageBuilder(route_number).create_page(forward)

    route_url = f"http://127.0.0.1:8080/data/routes/{html_name}"
    await bot.send_message(chat_id=call.from_user.id,
                           text=f'[Посмотреть на Maps]({route_url})',
                           parse_mode=types.ParseMode.MARKDOWN)

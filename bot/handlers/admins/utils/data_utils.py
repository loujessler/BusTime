from aiogram import types
from aiogram.dispatcher.filters import Command

from bot.loader import dp, bot

from bot.utils.data_utils.json_data import save_stops_data, load_stops_data, save_stations_data
from bot.handlers.main.ttc.ttc_requests.stops_stations import fetch_stops_data


@dp.callback_query_handler(text='refresh_bus_stops_data')
async def update_stops(callback_query: types.CallbackQuery):
    # Получение данных об остановках от API
    stops_data, stations_data = await fetch_stops_data()
    # Сохранение данных об остановках в JSON-файле
    save_stops_data(stops_data)
    save_stations_data(stations_data)
    await bot.answer_callback_query(callback_query.id, 'Данные об остановках обновлены', show_alert=True)


@dp.message_handler(Command("stops", prefixes="/"), is_admin=True)
async def show_stops(message: types.Message):
    stops_data = load_stops_data()

    stops_text = ""
    for stop in stops_data:
        stops_text += f'CODE: {stop["code"]}, ID: {stop["id"]}, Name: {stop["name"]}, Latitude: {stop["lat"]}, Longitude: {stop["lon"]}\n'

    # if len(stops_text) > 4096:
    #     stops_text = stops_text[:4060] + '... (too long to display all)'

    # await bot.send_message(message.chat.id, stops_text)

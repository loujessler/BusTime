import asyncio

from aiogram import types
from aiogram.dispatcher.filters import Command

from bot.handlers.admins.admin_menu import admin_menu
from bot.loader import dp, bot

from bot.utils.data_utils.json_data import save_json_data, load_json_data
from bot.handlers.main.ttc.ttc_requests.get_ttc_api import GetTTC


@dp.callback_query_handler(text='refresh_json_data', is_admin=True)
async def update_stops(call: types.CallbackQuery):
    # Получение данных об остановках от API
    get_ttc = GetTTC(call)
    stops_data, stations_data = await get_ttc.fetch_stops_data()
    buses_data = await get_ttc.fetch_bus_data()
    # Сохранение данных об остановках в JSON-файле
    data_dict = {'stops_data': stops_data,
                 'stations_data': stations_data,
                 'buses_data': buses_data}
    for data_name, data in data_dict.items():
        await save_json_data(data_name, data)

    await bot.answer_callback_query(call.id, 'JSON Данные обновлены', show_alert=True)
    await admin_menu(call)


@dp.callback_query_handler(text='refresh_json_bus_routes', is_admin=True)
async def update_stops(call: types.CallbackQuery):
    # Получение данных об остановках от API
    get_ttc = GetTTC(call)
    buses = await load_json_data('buses_data', 'RouteNumber')
    for bus in buses:
        for foward in [0, 1]:
            bus_route = await get_ttc.fetch_bus_route_info(bus, foward)
            # Сохранение данных об остановках в JSON-файле
            await save_json_data(f"routes/{bus_route[0]}", bus_route[1])

    msg_done = await bot.send_message(call.from_user.id, 'JSON Данные обновлены')
    await asyncio.sleep(3)
    await bot.delete_message(call.from_user.id, msg_done.message_id)
    await admin_menu(call)


@dp.message_handler(Command("stops", prefixes="/"), is_admin=True)
async def show_stops(message: types.Message):
    stops_data = await load_json_data('stops_data')

    stops_text = ""
    for stop in stops_data:
        stops_text += f'CODE: {stop["code"]}, ID: {stop["id"]}, Name: {stop["name"]}, ' \
                      f'Latitude: {stop["lat"]}, Longitude: {stop["lon"]}\n'

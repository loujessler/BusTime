from aiogram.dispatcher.filters import Command

from bot.loader import dp, bot
import httpx
from aiogram import types
import folium
import os


async def fetch_route_info(route_number, forward):
    url = f"http://transfer.ttc.com.ge:8080/otp/routers/ttc/routeInfo?routeNumber={route_number}&type=bus&forward={forward}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
    data = resp.json()

    shape = data['Shape']
    coordinates = shape.split(",")
    coordinates = [(float(c.split(":")[1]), float(c.split(":")[0])) for c in coordinates]

    stops = data['RouteStops']
    stop_info = [(float(stop['Lat']), float(stop['Lon']), stop['StopId']) for stop in stops]

    return coordinates, stop_info


@dp.message_handler(Command("map", prefixes="/"))
async def command_start(message: types.Message):
    # route_number = message.text
    route_number = '364'
    forward = '0'  # forward If true, returns the stops for the route in the forward direction.

    existing_files = os.path.exists(f'data/routes/{route_number}_{forward}.html')
    if existing_files:
        # If file already exists, just send the first match
        html_name = f'{route_number}_{forward}.html'
    else:
        # Fetch the route data and generate the map
        coordinates, stop_info = await fetch_route_info(route_number, forward)

        m = folium.Map(location=coordinates[0], zoom_start=14)
        folium.PolyLine(coordinates, color="#3d00f7", weight=2.5, opacity=1).add_to(m)
        for stop in stop_info:
            folium.Marker(location=(stop[0], stop[1]), popup=f"Stop ID: {stop[2]}").add_to(m)
        m.fit_bounds(coordinates)  # Automatically adjust map to show the whole route

        html_name = f"{route_number}_{forward}.html"
        m.save(os.path.join('data', 'routes', html_name))
    route_url = f"http://127.0.0.1:8080/data/routes/{html_name}"
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'[Посмотреть на Maps]({route_url})',
                           parse_mode=types.ParseMode.MARKDOWN)

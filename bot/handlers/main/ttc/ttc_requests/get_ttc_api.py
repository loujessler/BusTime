from typing import List, Callable, Any, Coroutine
import asyncio
import httpx
import xmltodict
from aiogram import types

from loguru import logger
from transliterate import translit

from bot.loader import bot
from bot.keyboards.inline.inline_kb_default import ikb_default
from bot.utils.additional import return_msg_aio_type, capitalize_words
from bot.utils.preloader import show_loading_message
from bot.utils.edit_last_message import EditLastMessage
from data.messages.arrival_messages import ArrivalMessages

edit_ls = EditLastMessage(bot)


class GetTTC:
    def __init__(self):
        self.ttc_url = "http://transfer.ttc.com.ge:8080/otp/routers/ttc"

    @staticmethod
    async def _make_asyncio_tasks(tasks: List[Coroutine[Any, Any, Any]]) -> List[Any]:
        # Создаем задачи для каждой функции в списке
        task_objs = [asyncio.create_task(task) for task in tasks]
        await asyncio.wait(task_objs)
        return [task.result() for task in task_objs]

    async def get_api_response(self, url: str, event=None, json: bool = False):
        client = httpx.AsyncClient(timeout=20.0)
        try:
            response = await client.get(url=self.ttc_url + url)
            response.raise_for_status()  # This will raise an exception for 4xx and 5xx status codes
            return response.json() if json else response
        except httpx.HTTPStatusError as e:
            logger.warning(f'Error while executing request: {e}')
            return None  # Return or assign default value when an error occurs
        except httpx.ReadTimeout:
            logger.warning("The request to the server has timed out. Please try again later.")
            return None  # Return or assign default value when an error occurs
        finally:
            await client.aclose()
            if event is not None:
                event.set()

    async def _load_get_api_tasks(self, aio_type, url: str, json: bool = False):
        event = asyncio.Event()
        tasks = [show_loading_message(aio_type, event),  self.get_api_response(url, event, json)]
        return (await self._make_asyncio_tasks(tasks))[1]

    # Даныые о рсаписании автобусов
    async def arrival(self, aio_type, code_bus_stop: str):
        user = aio_type.conf.get('user')
        url = f'/stopArrivalTimes?stopId={code_bus_stop}'
        message = await return_msg_aio_type(aio_type)
        json_data = await self._load_get_api_tasks(message, url, True)

        if not isinstance(json_data, dict):
            logger.warning('Unexpected data type for json_data: ' + str(type(json_data)))
            return

        if json_data is None:
            print("WARNING")
            return

        arrival_time_key = 'ArrivalTime'
        if arrival_time_key not in json_data:
            logger.warning(f'{arrival_time_key} key not found in JSON data')
            return

        arrival_times = json_data[arrival_time_key]
        msg = ArrivalMessages(user, arrival_times, code_bus_stop)
        language = user.language

        if len(arrival_times):
            message_data = [await msg.bus_arrival_times(), ikb_default(
                language, {
                    'refresh': f'stop_{code_bus_stop}',
                    'notification': 'notification',
                    'back_to_main_menu': 'back_to_main_menu',
                })]
        else:
            message_data = [await msg.bus_arrival_not(), ikb_default(
                language, {
                    'refresh': f'stop_{code_bus_stop}',
                    'back_to_main_menu': 'back_to_main_menu',
                })]

        if 'message_data' in locals():
            await edit_ls.edit_last_message(message_data[0], aio_type, message_data[1], types.ParseMode.MARKDOWN)
        # LOGS
        logger.log(25, f"The user {aio_type.from_user.id} receives the schedule from {code_bus_stop}.")

    # Берем данные о остановках
    async def fetch_stops_data(self, aio_type) -> list:
        url = f"/index/stops"
        message = await return_msg_aio_type(aio_type)
        json_data = await self._load_get_api_tasks(message, url, True)

        # Отделяем остановки от станций одним проходом
        stops, stations = [], []
        for item in json_data:
            item['name_translit'] = await capitalize_words(translit(item['name'], 'ka', reversed=True))
            if 'code' in item and item['code'].isdigit():
                stops.append(item)
            else:
                stations.append(item)

        # Сортируем и сохраняем данные в разные файлы
        stops.sort(key=lambda x: int(x['code']))
        stations.sort(key=lambda x: x['id'].split(":")[1])

        return [stops, stations]

    # Данные о всех транспортных средств
    async def fetch_bus_data(self, aio_type) -> list:
        url = f"/routes"
        message = await return_msg_aio_type(aio_type)
        xml_data = (await self._load_get_api_tasks(message, url, True)).text

        # Преобразуем XML в словарь
        data_dict = xmltodict.parse(xml_data)

        buses = []
        for route in data_dict['routeInfoes']['Route']:
            if route['Type'] != 'bus':
                continue

            item = {
                'Color': route['Color'],
                'Id': route['Id'],
                'LongName': route['LongName'],
                'LongName_translit': await capitalize_words(translit(route['LongName'], 'ka', reversed=True)),
                'RouteNumber': route['RouteNumber'],
                'StopA': route['StopA'],
                'StopB': route['StopB'],
                'StopA_translit': await capitalize_words(translit(route['StopA'], 'ka', reversed=True)),
                'StopB_translit': await capitalize_words(translit(route['StopB'], 'ka', reversed=True)),
                'Type': route['Type'],
            }

            buses.append(item)

        # Сортируем и сохраняем данные
        buses.sort(key=lambda x: x['RouteNumber'])

        return buses

    # Данные о маршрутах автобусов
    async def fetch_bus_route_info(self, route_number: str, forward: int) -> list:
        url = f"/routeInfo?routeNumber={route_number}&type=bus&forward={forward}"
        json_data = await self.get_api_response(url=url, json=True)

        # Отделяем остановки от станций одним проходом
        bus_route_stops = []
        name_bus = f"{json_data['RouteNumber']}_forward_{forward}"

        bus_route = {k: json_data[k] for k in ['Id', 'Type', 'RouteNumber', 'LongName', 'Color', 'Shape']}

        for item in json_data['RouteStops']:
            item['Name_translit'] = await capitalize_words(translit(item['Name'], 'ka', reversed=True))
            bus_route_stops.append(item)

        bus_route['RouteStops'] = bus_route_stops

        return [name_bus, bus_route]

    async def where_bus_info(self, route_number: str, forward: str) -> list:
        url = f"/buses?routeNumber={route_number}&forward={forward}"
        json_data = await self.get_api_response(url=url, json=True)

        locations = []
        for location in json_data['bus']:
            locations.append([location['lat'], location['lon']])
        return locations

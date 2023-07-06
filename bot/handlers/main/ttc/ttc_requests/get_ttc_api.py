import asyncio
import httpx
import xmltodict

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
    def __init__(self, aio_type):
        self.aio_type = aio_type
        self.user_id = self.aio_type.from_user.id
        self.user = self.aio_type.conf.get('user')
        self.language = self.user.language
        self.message = None

    @staticmethod
    async def get_api_response(url: str, event=None, json: bool = False):
        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                response = await client.get(url)
                response.raise_for_status()  # This will raise an exception for 4xx and 5xx status codes
                if json is True:
                    return response.json()
                else:
                    return response
        except httpx.HTTPStatusError as e:
            logger.warning(f'Error while executing request: {e}')
            return None  # Return or assign default value when an error occurs
        except httpx.ReadTimeout:
            logger.warning("The request to the server has timed out. Please try again later.")
            return None  # Return or assign default value when an error occurs
        finally:
            if event is not None:
                event.set()

    # Даныые о рсаписании автобусов
    async def arrival(self, code_bus_stop: str):
        message = await return_msg_aio_type(self.aio_type)
        chat_id = message.chat.id
        url = f'http://transfer.ttc.com.ge:8080/otp/routers/ttc/stopArrivalTimes?stopId={code_bus_stop}'

        event = asyncio.Event()
        loading_task = asyncio.create_task(show_loading_message(message, event))
        response_task = asyncio.create_task(self.get_api_response(url, event, True))
        await asyncio.wait([loading_task, response_task])
        json_data = response_task.result()

        if json_data is None:
            print("WARNING")
            return

        arrival_time_key = 'ArrivalTime'
        if arrival_time_key not in json_data:
            logger.warning(f'{arrival_time_key} key not found in JSON data')
            return

        arrival_times = json_data[arrival_time_key]
        msg = ArrivalMessages(self.user, arrival_times, code_bus_stop)

        if len(arrival_times):
            message_data = [await msg.bus_arrival_times(), ikb_default(
                self.language, {
                    'refresh': f'stop_{code_bus_stop}',
                    'notification': 'notification',
                    'back_to_main_menu': 'back_to_main_menu',
                })]
        else:
            message_data = [await msg.bus_arrival_not(), ikb_default(
                self.language, {
                    'refresh': f'stop_{code_bus_stop}',
                    'back_to_main_menu': 'back_to_main_menu',
                })]

        if 'message_data' in locals():
            await edit_ls.edit_last_message(message_data[0], self.aio_type, message_data[1])

        # LOGS
        logger.log(25, f"The user {self.user_id} receives the schedule from {code_bus_stop}.")

    # Берем данные о остановках
    async def fetch_stops_data(self):
        url = "http://transfer.ttc.com.ge:8080/otp/routers/ttc/index/stops"
        message = await return_msg_aio_type(self.aio_type)

        event = asyncio.Event()
        loading_task = asyncio.create_task(show_loading_message(message, event))
        response_task = asyncio.create_task(self.get_api_response(url, event, True))
        await asyncio.wait([loading_task, response_task])
        json_data = response_task.result()

        # Отделяем остановки от станций одним проходом
        stops = []
        stations = []
        for item in json_data:
            item['name_translit'] = await capitalize_words(translit(item['name'], 'ka', reversed=True))
            if 'code' in item and item['code'].isdigit():
                stops.append(item)
            else:
                stations.append(item)

        # Сортируем и сохраняем данные в разные файлы
        stops.sort(key=lambda item: int(item['code']))
        stations.sort(key=lambda item: item['id'].split(":")[1])

        return [stops, stations]

    # Данные о всех транспортных средств
    async def fetch_bus_data(self):
        url = "http://transfer.ttc.com.ge:8080/otp/routers/ttc/routes"
        message = await return_msg_aio_type(self.aio_type)

        event = asyncio.Event()
        loading_task = asyncio.create_task(show_loading_message(message, event))
        response_task = asyncio.create_task(self.get_api_response(url, event))
        await asyncio.wait([loading_task, response_task])
        xml_data = response_task.result().text

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
        buses.sort(key=lambda item: item['RouteNumber'])

        return buses

    # Данные о маршрутах автобусов
    async def fetch_bus_route_info(self, route_number, forward):
        url = f"http://transfer.ttc.com.ge:8080/otp/routers/ttc/routeInfo?routeNumber={route_number}&type=bus&forward={forward}"
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

# Version 1
# import asyncio
# from loguru import logger
# import httpx
#
# from bot.loader import bot
#
# from bot.keyboards.inline.inline_kb_default import ikb_default
#
# from bot.utils.additional import return_msg_aio_type
# from bot.utils.data_utils.json_data import load_stops_data
# from bot.utils.edit_last_message import EditLastMessage
# from bot.utils.db_api import quick_commands as commands
# from bot.utils.localization.i18n import MessageFormatter
#
# from data.messages.arrival_messages import ArrivalMessages
#
# edit_ls = EditLastMessage(bot)
#
#
# class GetAPISchedule:
#     def __init__(self, aio_type):
#         self.aio_type = aio_type
#
#     async def show_loading_message(self, aio_type, event):
#         loading_messages = ['🕐', '🕑', '🕒', '🕓', '🕔', '🕕', '🕖', '🕗', '🕘', '🕙', '🕚', '🕛']
#         chat_id = aio_type.chat.id
#         message = await bot.send_message(chat_id=chat_id, text=loading_messages[0])
#         await asyncio.sleep(0.5)
#
#         i = 1
#         while not event.is_set():
#             await bot.edit_message_text(text=loading_messages[i], chat_id=chat_id, message_id=message.message_id)
#             await asyncio.sleep(0.5)
#             i = (i + 1) % len(loading_messages)
#
#         await bot.delete_message(chat_id=chat_id, message_id=message.message_id)
#
#     async def arrival(self, code_bus_stop, aio_type):
#         message = await return_msg_aio_type(aio_type)
#         try:
#             await message.delete()
#         except:
#             pass
#         user_id = aio_type.from_user.id
#         user = aio_type.conf.get('user')
#         language = user.language
#
#         if str(code_bus_stop) not in load_stops_data('code'):
#             await edit_ls.edit_last_message(
#                 MessageFormatter(language).get_message({'arrival_bus_stop_not_exists': 'bold'}),
#                 aio_type,
#                 ikb_default(language, {
#                     'back_to_main_menu': 'back_to_main_menu',
#                 })
#             )
#         else:
#             chat_id = message.chat.id
#             url = f'http://transfer.ttc.com.ge:8080/otp/routers/ttc/stopArrivalTimes?stopId={code_bus_stop}'
#
#             try:
#                 event = asyncio.Event()
#                 loading_task = asyncio.create_task(show_loading_message(message, event))
#
#                 async with httpx.AsyncClient(timeout=20.0) as client:
#                     response = await client.get(url)
#                     response.raise_for_status()  # This will raise an exception for 4xx and 5xx status codes
#
#                 event.set()  # Устанавливаем событие, чтобы прервать выполнение функции show_loading_message
#                 await loading_task  # Дожидаемся завершения задачи show_loading_message
#
#                 json_data = response.json()
#
#                 arrival_time_key = 'ArrivalTime'
#
#                 if arrival_time_key not in json_data:
#                     await bot.send_message(chat_id, f'{arrival_time_key} key not found in JSON data')
#                     return
#
#                 arrival_times = json_data[arrival_time_key]
#                 num_arrival_times = len(arrival_times)
#                 msg = ArrivalMessages(user, arrival_times, code_bus_stop)
#
#                 if num_arrival_times:
#                     await edit_ls.edit_last_message(
#                         msg.bus_arrival_times(),
#                         aio_type,
#                         ikb_default(language, {
#                             'refresh': f'stop_{code_bus_stop}',
#                             'notification': 'notification',
#                             'back_to_main_menu': 'back_to_main_menu',
#                         })
#                     )
#                 else:
#                     await edit_ls.edit_last_message(
#                         msg.bus_arrival_not(),
#                         aio_type,
#                         ikb_default(language, {
#                             'refresh': f'stop_{code_bus_stop}',
#                             'back_to_main_menu': 'back_to_main_menu',
#                         })
#                     )
#
#             except httpx.HTTPStatusError as e:
#                 await bot.send_message(chat_id, f'Error while executing request: {e}')
#             except httpx.ReadTimeout:
#                 await bot.send_message(chat_id, "The request to the server has timed out. Please try again later.")
#         # LOGS
#         logger.log(25, f"The user {user_id} receives the schedule from {code_bus_stop}.")

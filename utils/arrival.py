import requests

from aiogram import types
from loader import bot
from utils.edit_last_message import EditLastMessage
from utils.db_api import quick_commands as commands

from data.messages.arrival_messages import ArrivalMessages

edit_ls = EditLastMessage(bot)


async def arrival(id_stop, aio_type):
    # Проверяем тип объекта и отправляем сообщение в чат
    if isinstance(aio_type, types.CallbackQuery):
        chat_id = aio_type.message.chat.id
    elif isinstance(aio_type, types.Message):
        chat_id = aio_type.chat.id
    else:
        return  # Выход из функции, если передан некорректный объект

    code_bus_stop = id_stop
    url = f'http://transfer.ttc.com.ge:8080/otp/routers/ttc/stopArrivalTimes?stopId={code_bus_stop}'
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()  # Получаем данные JSON
        # Проверяем наличие ключа 'ArrivalTime' и выводим его значение
        if 'ArrivalTime' in json_data:
            arrival_times = json_data['ArrivalTime']
            num_arrival_times = len(arrival_times)  # Находим длину arrival_times
            user = await commands.select_user(aio_type.from_user.id)
            msg = ArrivalMessages(user, arrival_times, code_bus_stop)
            if num_arrival_times:
                await bot.send_message(chat_id, msg.bus_arrival_times())
            else:
                await bot.send_message(chat_id, msg.bus_arrival_not())
        else:
            await bot.send_message(chat_id, 'ArrivalTime key not found in JSON data')
    else:
        await bot.send_message(chat_id, f'Error while executing request: {response.status_code}')

# async def arrival(id_stop, aio_type):
#     code_bus_stop = id_stop
#     url = f'http://transfer.ttc.com.ge:8080/otp/routers/ttc/stopArrivalTimes?stopId={code_bus_stop}'
#     response = requests.get(url)
#     if response.status_code == 200:
#         json_data = response.json()  # Получаем данные JSON
#         # Проверяем наличие ключа 'ArrivalTime' и выводим его значение
#         if 'ArrivalTime' in json_data:
#             arrival_times = json_data['ArrivalTime']
#             num_arrival_times = len(arrival_times)  # Находим длину arrival_times
#             user = await commands.select_user(aio_type.from_user.id)
#             msg = ArrivalMessages(user, arrival_times)
#             if num_arrival_times:
#                 await aio_type.answer(msg.bus_arrival_times())
#             else:
#                 await aio_type.answer(msg.bus_arrival_not())
#         else:
#             await aio_type.answer('ArrivalTime key not found in JSON data')
#     else:
#         await aio_type.answer(f'Error while executing request: {response.status_code}')
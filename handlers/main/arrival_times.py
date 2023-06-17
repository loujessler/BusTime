from aiogram import types
from aiogram.types import CallbackQuery

from loader import dp, bot

from utils.ttc_requests.arrival import arrival


# # Хэндлер для обработки текстовых сообщений
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_bus_stop_message(message: types.Message):
    # Получение текста сообщения
    text = message.text
    try:
        # Попытка преобразовать текст в целое число
        bus_stop_id = int(text)
        await arrival(bus_stop_id, message)
    except ValueError:
        pass


@dp.callback_query_handler(text_startswith='stop_')
async def call_handler_stop(call: CallbackQuery):
    # Получаем данные из обратного вызова
    callback_data = call.data
    splitted_data = callback_data.split('_')
    code_bus_stop = splitted_data[1]
    if len(splitted_data) > 2:
        if splitted_data[2] == 'wmap':
            await bot.delete_message(call.message.chat.id, splitted_data[3])
    if int(code_bus_stop):
        await arrival(code_bus_stop, call)

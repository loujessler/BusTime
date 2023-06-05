from aiogram import types
from aiogram.types import CallbackQuery

from loader import dp

from utils.arrival import arrival


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
    text = callback_data.split('_')[1]
    if int(text):
        await arrival(text, call)

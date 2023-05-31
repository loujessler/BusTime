from aiogram.types import CallbackQuery

from loader import dp, bot
from aiogram import types

from utils.arrival import arrival


# Хэндлер для обработки текстовых сообщений
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_bus_stop_message(message: types.Message):
    # Получение текста сообщения
    text = message.text
    if int(text):
        await arrival(text, message)


@dp.callback_query_handler(text_startswith='stop_')
async def call_handler_stop(call: CallbackQuery):
    # Получаем данные из обратного вызова
    callback_data = call.data
    text = callback_data.split('_')[1]
    if int(text):
        await arrival(text, call)

from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters import Regexp

from bot.loader import dp, bot

from bot.handlers.main.ttc.ttc_requests.get_ttc_api import GetTTC


# # Хэндлер для обработки текстовых сообщений
@dp.message_handler(Regexp(r'^\d+$'), is_bus_stop=True)
async def handle_bus_stop_message(message: types.Message):
    await message.delete()
    await GetTTC().arrival(message, message.text)


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
        await GetTTC().arrival(call, code_bus_stop)

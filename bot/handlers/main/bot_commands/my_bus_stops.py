from aiogram import types
from aiogram.dispatcher.filters import Command

from bot.loader import dp, bot
from bot.utils.my_bus_stops import my_bus_stops


@dp.message_handler(Command('my_bus_stops'))
async def message_my_bus_stops(message: types.Message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await my_bus_stops(message)

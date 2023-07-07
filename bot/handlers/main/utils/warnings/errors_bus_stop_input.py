import asyncio
from aiogram import types

from bot.loader import bot
from bot.utils.localization.i18n import MessageFormatter


async def error_regexp(message: types.Message):
    user = message.conf.get('user')
    msg = MessageFormatter(user.language, 'warning').get_message({'only_digit': 'none'})
    await message.delete()
    msg_for_del = await bot.send_message(message.chat.id, msg)
    await asyncio.sleep(5)
    await bot.delete_message(message.chat.id, msg_for_del.message_id)


async def error_bus_stop(message: types.Message):
    user = message.conf.get('user')
    msg = MessageFormatter(user.language, 'warning').get_message({'dont_have_bus_stop': 'none'})
    await message.delete()
    msg_for_del = await bot.send_message(message.chat.id, msg)
    await asyncio.sleep(5)
    await bot.delete_message(message.chat.id, msg_for_del.message_id)
from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from bot.utils.db_api import quick_commands as commands


class GetUserMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        user = await commands.select_user(message)
        message.conf["user"] = user

    async def on_pre_process_callback_query(self, call: types.CallbackQuery, data: dict):
        user = await commands.select_user(call)
        call.conf["user"] = user

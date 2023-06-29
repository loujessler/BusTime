from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from collections import defaultdict
import time

from bot.utils.db_api import quick_commands as commands
from bot.utils.localization.i18n import MessageFormatter


class AntiSpamMiddleware(BaseMiddleware):
    def __init__(self):
        self.user_time = defaultdict(int)
        self.user_spam_counter = defaultdict(int)
        self.spam_time = 1  # время в секундах между сообщениями
        self.max_spam_count = 4  # максимальное количество сообщений в течении времени spam_time
        self.block_time = 600  # время блокировки в секундах (10 минут)
        self.blocked_until = defaultdict(int)
        super().__init__()

    async def on_pre_process_message(self, message: types.Message, data: dict):
        current_time = round(time.time())

        # Проверка, является ли сообщение командой /cancel
        if message.text == "/cancel":
            return

        user = await commands.select_user(message)
        formatter = MessageFormatter(user.language, 'warning')

        # Если пользователь заблокирован
        if current_time < self.blocked_until[message.from_user.id]:
            await message.answer(formatter.get_message({'you are block': 'italic'}))
            raise CancelHandler()

        # Если прошло достаточно времени с последнего сообщения
        if current_time - self.user_time[message.from_user.id] > self.spam_time:
            self.user_time[message.from_user.id] = current_time
            self.user_spam_counter[message.from_user.id] = 1
        else:
            self.user_spam_counter[message.from_user.id] += 1
            if self.user_spam_counter[message.from_user.id] > self.max_spam_count:
                self.blocked_until[message.from_user.id] = current_time + self.block_time
                await message.answer(formatter.get_message({'block for ten min': 'italic'}))
                raise CancelHandler()
            else:
                await message.answer(formatter.get_message({'many messages': 'italic'}))
                raise CancelHandler()

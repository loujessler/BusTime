from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from bot.utils.data_utils.json_data import load_json_data


class IsBus(BoundFilter):
    key = "is_bus"

    def __init__(self, is_bus):
        self.is_bus = is_bus

    async def check(self, message: types.Message):
        result = message.text in await load_json_data('buses_data', 'RouteNumber')
        return result if self.is_bus else not result

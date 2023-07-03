from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from bot.utils.data_utils.json_data import load_json_data


class IsBusStop(BoundFilter):
    key = "is_bus_stop"

    def __init__(self, is_bus_stop):
        self.is_bus_stop = is_bus_stop

    async def check(self, message: types.Message):
        result = message.text in await load_json_data('stops_data', 'code')
        return result if self.is_bus_stop else not result


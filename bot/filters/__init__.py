from aiogram import Dispatcher

from .private_chat import IsPrivate
from .is_admin import IsAdmin
from .is_bus import IsBus
from .is_bus_stop import IsBusStop


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(IsBus)
    dp.filters_factory.bind(IsBusStop)
    dp.filters_factory.bind(IsPrivate)

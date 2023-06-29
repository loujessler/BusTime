from aiogram import Dispatcher

from .private_chat import IsPrivate
from .is_admin import IsAdmin


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(IsPrivate)

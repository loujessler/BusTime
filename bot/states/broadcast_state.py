from aiogram.dispatcher.filters.state import StatesGroup, State


class BroadcastStates(StatesGroup):
    msg = State()

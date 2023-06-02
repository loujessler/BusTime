from aiogram.dispatcher.filters.state import StatesGroup, State


class Regist(StatesGroup):
    language = State()
    change_language = State()
    name_bus_stops_state = State()
    id_bus_stops_state = State()
    delete_bus_stop = State()
    msg = State()

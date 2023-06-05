import asyncio

from aiogram.dispatcher.filters.state import StatesGroup, State

from keyboards.inline.inline_kb_default import ikb_default
from loader import bot
from utils.i18n import MessageFormatter


class Regist(StatesGroup):
    locale = State()
    language = State()
    change_language = State()
    name_bus_stops_state = State()
    id_bus_stops_state = State()
    delete_bus_stop = State()
    msg = State()


class TimeRegistrate:
    def __init__(self, state, send_message, user):
        self.state = state
        self.sent_message = send_message
        self.user = user

    async def on_timeout(self):
        await bot.delete_message(self.sent_message.chat.id, self.sent_message.message_id)  # chat_id надо указать
        await self.state.finish()
        await self.sent_message.answer(
            text=MessageFormatter(self.user).get_message({'bus_stops_finish_cancel': 'none'}),
            reply_markup=ikb_default(self.user)
        )

    async def state_timer(self, timeout=30):
        # Подождите timeout секунд
        await asyncio.sleep(timeout)

        # Получение данных из состояния
        data = await self.state.get_data()
        state_name = await self.state.get_state('name')
        if state_name:
            state_name = state_name.split(':')[1]
        else:
            await self.state.finish()
        # Проверка, есть ли у нас нужные данные
        if state_name == 'name_bus_stops_state' and 'name' not in data:
            await self.on_timeout()

        if state_name == 'id_bus_stops_state' and 'id_stop' not in data:
            await self.on_timeout()

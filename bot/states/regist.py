from aiogram.dispatcher.filters.state import StatesGroup, State


class Regist(StatesGroup):
    locale = State()
    language = State()
    change_language = State()
    name_bus_stops_state = State()
    id_bus_stops_state = State()
    change_name_bus_stop = State()
    change_code_bus_stop = State()
    delete_bus_stop = State()
    msg = State()


# class TimeRegistrate:
#     def __init__(self, state, send_message, user):
#         self.state = state
#         self.sent_message = send_message
#         self.user = user
#
#     async def on_timeout(self, message_send: str):
#         aio_type = return_msg_aio_type(self.sent_message)
#         for i in range(4):
#             try:
#                 await bot.delete_message(aio_type.chat.id, aio_type.message_id + i)  # chat_id надо указать
#             except:
#                 pass
#         await self.state.finish()
#         await edit_ls.edit_last_message(
#             MessageFormatter(self.user.language).get_message({message_send: 'none'}),
#             aio_type, ikb_default(self.user)
#         )
#
#     async def state_timer(self, timeout=120):
#         # Подождите timeout секунд
#         await asyncio.sleep(timeout)
#
#         # Получение данных из состояния
#         data = await self.state.get_data()
#         state_name = await self.state.get_state('name')
#         if state_name:
#             state_name = state_name.split(':')[1]
#         # Проверка, есть ли у нас нужные данные
#         if state_name == 'name_bus_stops_state' and 'name' not in data:
#             await self.on_timeout('bus_stops_finish_cancel')
#         elif state_name == 'id_bus_stops_state' and 'id_stop' not in data:
#             await self.on_timeout('bus_stops_finish_cancel')
#         elif state_name == 'change_name_bus_stop' and 'name' not in data:
#             await self.on_timeout('change_name_bus_stops_cancel')
#         elif state_name == 'change_code_bus_stop' and 'stop_code' not in data:
#             await self.on_timeout('change_code_bus_stops_cancel')

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp, bot
from filters import HaveInDb

from data.messages.bus_stops_messages import BusStopsMSG

from keyboards.inline.bus_stops import ikb_menu_bus_stops

from states.regist import Regist

from utils.db_api import quick_commands as commands
from utils.my_bus_stops import my_bus_stops

from handlers.main.bot_start import edit_ls


@dp.callback_query_handler(text='my_bus_stops')
async def callback_my_bus_stops(message: types.Message):
    await my_bus_stops(message)


@dp.message_handler(HaveInDb(True), Command('my_bus_stops'))
async def message_my_bus_stops(message: types.Message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await my_bus_stops(message)


@dp.callback_query_handler(text='add_new_bus_stop')
async def set_name_bus_stops(message: types.Message):
    user = await commands.select_user(message.from_user.id)
    await edit_ls.edit_last_message(
                BusStopsMSG(user).get_message('name'),
                message
            )
    await Regist.name_bus_stops_state.set()


@dp.message_handler(HaveInDb(True), state=Regist.name_bus_stops_state)
async def number_bus_stop(message: types.Message, state: FSMContext):
    user = await commands.select_user(message.from_user.id)
    await state.update_data(name=message.text)
    await bot.delete_message(message.from_user.id, message.message_id)
    await edit_ls.edit_last_message(
        BusStopsMSG(user).get_message('id_stop'),
        message
    )
    await Regist.id_bus_stops_state.set()


@dp.message_handler(HaveInDb(True), state=Regist.id_bus_stops_state)
async def create_fav_bus_stop(message: types.Message, state: FSMContext):
    user = await commands.select_user(message.from_user.id)
    await state.update_data(id_stop=message.text)
    data = await state.get_data()
    name = data.get('name')
    id_stop = data.get('id_stop')
    await bot.delete_message(message.from_user.id, message.message_id)
    # Если остановки отсутствуют, добавляем тестовую остановку
    await commands.add_bus_stop(user, name=name, id_stop=int(id_stop))
    bus_stops = await commands.select_all_bus_stops(user)
    if bus_stops:
        await edit_ls.edit_last_message(
            BusStopsMSG(user).finish_add_stop(name, id_stop),
            message, ikb_menu_bus_stops(user, bus_stops)
        )
    else:
        await edit_ls.edit_last_message(
            BusStopsMSG(user).finish_add_stop(name, id_stop),
            message
        )
    await state.finish()


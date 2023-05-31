from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

# from data.messages.messages import Messages
from data.messages.start_messages import Messages
from data.messages.bus_stops_messages import BusStopsMSG
from filters import HaveInDb
from keyboards.inline import ikb_menu
from keyboards.inline.bus_stops import ikb_menu_bus_stops
from loader import dp, bot
from states.regist import Regist
from utils.db_api import quick_commands as commands
from handlers.main.bot_start import edit_ls
from utils.db_api.schemes.bus_stops import BusStop


@dp.message_handler(Command('my_bus_stops'), HaveInDb(True))
async def my_bus_stops(message: types.Message):
    user = await commands.select_user(message.from_user.id)
    await message.delete()
    if user:
        bus_stops = await commands.select_all_bus_stops(user)
        print(f'BUS STOPS: {bus_stops}')
        if bus_stops:
            # for bus_stop in bus_stops:
            #     print(f"Bus Stop: {bus_stop.name}, ID: {bus_stop.id_stop}")
            # await edit_ls.edit_last_message(
            #     BusStopsMSG(user).choose_bus_stop[user.language],
            #     message, ikb=ikb_menu_bus_stops(bus_stops)
            # )
            await message.answer(BusStopsMSG(user).choose_bus_stop[user.language],
                                 reply_markup=ikb_menu_bus_stops(user, bus_stops),
                                 parse_mode='HTML')
        else:
            await edit_ls.edit_last_message(
                BusStopsMSG(user).no_bus_stops[user.language],
                message
            )
            await Regist.name_bus_stops_state.set()


@dp.callback_query_handler(text='add_new_bus_stop')
async def my_bus_stops(message: types.Message):
    user = await commands.select_user(message.from_user.id)
    await edit_ls.edit_last_message(
                BusStopsMSG(user).name[user.language],
                message
            )
    await Regist.name_bus_stops_state.set()


@dp.message_handler(HaveInDb(True), state=Regist.name_bus_stops_state)
async def number_bus_stop(message: types.Message, state: FSMContext):
    user = await commands.select_user(message.from_user.id)
    await state.update_data(name=message.text)
    await bot.delete_message(message.from_user.id, message.message_id)
    await edit_ls.edit_last_message(
        BusStopsMSG(user).id_stop[user.language],
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


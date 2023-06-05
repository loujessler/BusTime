import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Regexp

from loader import dp, bot
from filters import HaveInDb

from keyboards.inline.bus_stops import ikb_menu_bus_stops

from states.regist import Regist, TimeRegistrate

from utils.db_api import quick_commands as commands
from utils.i18n import MessageFormatter
from utils.my_bus_stops import my_bus_stops

from handlers.main.bot_start import edit_ls


@dp.callback_query_handler(text='my_bus_stops')
async def callback_my_bus_stops(message: types.Message, state: FSMContext):
    await my_bus_stops(message, state)


@dp.message_handler(HaveInDb(True), Command('my_bus_stops'))
async def message_my_bus_stops(message: types.Message, state: FSMContext):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await my_bus_stops(message, state)


# Игнорирование состояния при определенных состояниях
@dp.message_handler(Regexp("^/"), state=Regist.name_bus_stops_state)
@dp.message_handler(Regexp("^/"), state=Regist.id_bus_stops_state)
async def ignore_commands_in_state(message: types.Message):
    await message.delete()
    response = await message.answer("Commands are not allowed in the current state.")
    await asyncio.sleep(5)
    await bot.delete_message(chat_id=response.chat.id, message_id=response.message_id)


@dp.message_handler(HaveInDb(True), Regexp(r'^[^\d]+$'), state=Regist.id_bus_stops_state)
async def ignore_text_in_id_bus_stops_state(message: types.Message, state: FSMContext):
    await message.delete()
    response = await message.answer("Commands are not allowed in the current state.")
    await asyncio.sleep(5)
    await bot.delete_message(chat_id=response.chat.id, message_id=response.message_id)


@dp.callback_query_handler(text='add_new_bus_stop')
async def set_name_bus_stops(call: types.CallbackQuery, state: FSMContext):
    user = await commands.select_user(call.from_user.id)
    asyncio.create_task(TimeRegistrate(state, call, user).state_timer())
    sent_message = await edit_ls.edit_last_message(
        MessageFormatter(user).get_message({'bus_stops_name': 'none'}),
        call, None, 'HTML', True
    )
    Regist.name_bus_stops_state.message_id = sent_message.message_id  # Сохраняем message_id
    await Regist.name_bus_stops_state.set()


@dp.message_handler(HaveInDb(True), state=Regist.name_bus_stops_state)
async def number_bus_stop(message: types.Message, state: FSMContext):
    user = await commands.select_user(message.from_user.id)
    asyncio.create_task(TimeRegistrate(state, message, user).state_timer())
    await state.update_data(name=message.text)
    await bot.delete_message(message.from_user.id, message.message_id)
    await bot.delete_message(message.from_user.id,
                             Regist.name_bus_stops_state.message_id)  # Используйте message_id отсюда
    sent_message = await edit_ls.edit_last_message(
        MessageFormatter(user).get_message({'bus_stops_id_stop': 'none'}),
        message, None, 'HTML', True
    )
    Regist.id_bus_stops_state.message_id = sent_message.message_id
    await Regist.id_bus_stops_state.set()


@dp.message_handler(HaveInDb(True), state=Regist.id_bus_stops_state)
async def create_fav_bus_stop(message: types.Message, state: FSMContext):
    user = await commands.select_user(message.from_user.id)
    asyncio.create_task(TimeRegistrate(state, message, user).state_timer())
    id_stop = int(message.text)
    if 0 <= id_stop <= 100000:
        await state.update_data(id_stop=message.text)
        data = await state.get_data()
        name = data.get('name')
        message_id = data.get('message_id')
        # await bot.delete_message(message.from_user.id, message_id)
        await bot.delete_message(message.from_user.id, message.message_id)
        await bot.delete_message(message.from_user.id, Regist.id_bus_stops_state.message_id)
        await commands.add_bus_stop(user, name=name, id_stop=id_stop)
        bus_stops = await commands.select_all_bus_stops(user)
        msg_f = MessageFormatter(user)
        if bus_stops:
            await edit_ls.edit_last_message(
                msg_f.get_message({'bus_stops_finish_add_stop': 'none'},
                                  {'name': name, 'id_stop': id_stop}),
                message, ikb_menu_bus_stops(user, bus_stops)
            )
        else:
            await edit_ls.edit_last_message(
                msg_f.get_message({'bus_stops_finish_cancel': 'none'}),
                message
            )
        await state.finish()
    else:
        await message.answer("Please input a number between 0 and 100000.")

# @dp.callback_query_handler(text='add_new_bus_stop')
# async def set_name_bus_stops(message: types.Message):
#     user = await commands.select_user(message.from_user.id)
#     await edit_ls.edit_last_message(
#         MessageFormatter(user).get_message({'bus_stops_name': 'none'}),
#         message
#     )
#     await Regist.name_bus_stops_state.set()
#
#
# @dp.message_handler(HaveInDb(True), state=Regist.name_bus_stops_state)
# async def number_bus_stop(message: types.Message, state: FSMContext):
#     user = await commands.select_user(message.from_user.id)
#     await state.update_data(name=message.text)
#     await bot.delete_message(message.from_user.id, message.message_id)
#     await edit_ls.edit_last_message(
#         MessageFormatter(user).get_message({'bus_stops_id_stop': 'none'}),
#         message
#     )
#     await Regist.id_bus_stops_state.set()
#
#
# @dp.message_handler(HaveInDb(True), state=Regist.id_bus_stops_state)
# async def create_fav_bus_stop(message: types.Message, state: FSMContext):
#     user = await commands.select_user(message.from_user.id)
#     id_stop = int(message.text)
#     if 0 <= id_stop <= 100000:
#         await state.update_data(id_stop=message.text)
#         data = await state.get_data()
#         name = data.get('name')
#         await bot.delete_message(message.from_user.id, message.message_id)
#         await commands.add_bus_stop(user, name=name, id_stop=id_stop)
#         bus_stops = await commands.select_all_bus_stops(user)
#         msg_f = MessageFormatter(user)
#         if bus_stops:
#             await edit_ls.edit_last_message(
#                 msg_f.get_message({'bus_stops_finish_add_stop': 'none'},
#                                   {'name': name, 'id_stop': id_stop}),
#                 message, ikb_menu_bus_stops(user, bus_stops)
#             )
#         else:
#             await edit_ls.edit_last_message(
#                 msg_f.get_message({'bus_stops_finish_add_stop': 'none'},
#                                   {'name': name, 'id_stop': id_stop}),
#                 message
#             )
#         await state.finish()
#     else:
#         await message.answer("Please input a number between 0 and 100000.")

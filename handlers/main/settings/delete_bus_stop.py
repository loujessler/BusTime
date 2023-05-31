from aiogram.dispatcher import FSMContext

from filters import HaveInDb
from keyboards.inline.bus_stops import ikb_menu_bus_stops
from keyboards.inline.settings import ikb_back_to_settings
from loader import dp, bot
from aiogram import types

from data.messages.settings_messages import Messages
from states.regist import Regist
from utils.db_api import quick_commands as commands
from handlers.main.bot_start import edit_ls


@dp.callback_query_handler(HaveInDb(True), text='delete_bus_stop')
async def choose_stop(call: types.CallbackQuery):
    user = await commands.select_user(call.from_user.id)
    bus_stops = await commands.select_all_bus_stops(user)
    await edit_ls.edit_last_message(
        Messages.choose_bus_stop[user.language],
        call, ikb_menu_bus_stops(user, bus_stops)
    )
    await Regist.delete_bus_stop.set()


@dp.callback_query_handler(HaveInDb(True), state=Regist.delete_bus_stop)
async def create_password(call: types.CallbackQuery, state: FSMContext):
    user = await commands.select_user(call.from_user.id)
    callback_data = call.data.split('_')
    id_unique = int(callback_data[2])
    id_stop = callback_data[1]
    name = call.message.reply_markup.inline_keyboard[0][0]['text']
    delete_stop = await commands.delete_bus_stop(user, id_unique)
    print("delete_stop: ", delete_stop)
    if delete_stop:
        await edit_ls.edit_last_message(
            Messages.delete_stop_true[user.language],
            call, ikb_back_to_settings(user)
        )
    else:
        await edit_ls.edit_last_message(
            Messages.delete_stop_false[user.language],
            call, ikb_back_to_settings(user)
        )
    await state.finish()

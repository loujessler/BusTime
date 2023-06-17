from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup

from keyboards.inline.inline_kb_default import ikb_default
from loader import dp
from filters import HaveInDb

from keyboards.inline.bus_stops import ikb_menu_bus_stops

from states.regist import Regist
from utils.db_api import quick_commands as commands

from handlers.main.settings.settings_menu import handler_settings_menu
from handlers.main.inline_handlers.inline_back import handler_back
from handlers.main.bot_start import edit_ls
from utils.localization.i18n import MessageFormatter


@dp.callback_query_handler(HaveInDb(True), text='delete_bus_stop')
async def choose_stop(call: types.CallbackQuery):
    user = await commands.select_user(call.from_user.id)
    bus_stops = await commands.select_all_bus_stops(user)

    # Объединяем клавиатуры
    ikb = InlineKeyboardMarkup(row_width=2)
    ikb.inline_keyboard = ikb_menu_bus_stops(
        user,
        bus_stops,
        False).inline_keyboard + ikb_default(user,
                                             {'back_to_settings': 'back_to_settings',
                                              'back_to_main_menu': 'back_to_main_menu'
                                              }).inline_keyboard

    await edit_ls.edit_last_message(
        MessageFormatter(user.language).get_message({'setting_choose_bus_stop': 'bold'}),
        call, ikb
    )
    await Regist.delete_bus_stop.set()


@dp.callback_query_handler(HaveInDb(True), state=Regist.delete_bus_stop)
async def handler_delete_bus_stop(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'back_to_main_menu':
        # Here call your function or handler for 'back'
        await handler_back(call)
        await state.finish()
        return

    if call.data == 'back_to_settings':
        # Here call your function or handler for 'add_new_bus_stop'
        await handler_settings_menu(call)
        await state.finish()
        return

    user = await commands.select_user(call.from_user.id)

    callback_data = call.data.split('_')
    id_unique = int(callback_data[2])
    id_stop = callback_data[1]
    name = call.message.reply_markup.inline_keyboard[0][0]['text']
    delete_stop = await commands.delete_bus_stop(user, id_unique)
    msg_f = MessageFormatter(user.language)
    if delete_stop:
        await edit_ls.edit_last_message(
            msg_f.get_message({'setting_delete_stop_true': 'bold'}),
            call, ikb_default(user, {'back_to_settings': 'back_to_settings',
                                     'back_to_main_menu': 'back_to_main_menu'})
        )
    else:
        await edit_ls.edit_last_message(
            msg_f.get_message({'setting_delete_stop_false': 'bold'}),
            call, ikb_default(user, {'back_to_settings': 'back_to_settings',
                                     'back_to_main_menu': 'back_to_main_menu'})
        )
    await state.finish()


# Then in the handler for 'back'
@dp.callback_query_handler(text='back', state='*')
async def back_handler(call: types.CallbackQuery, state: FSMContext):
    # Check if the flag is set in the state data
    data = await state.get_data()
    if data.get('back_or_add_new_bus_stop') == 'back':
        # Perform the action for 'back' and then reset the flag
        await state.update_data(back_or_add_new_bus_stop=None)


# Similarly for 'add_new_bus_stop'
@dp.callback_query_handler(text='add_new_bus_stop', state='*')
async def add_new_bus_stop_handler(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data.get('back_or_add_new_bus_stop') == 'add_new_bus_stop':
        await state.update_data(back_or_add_new_bus_stop=None)

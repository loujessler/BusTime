import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot

from handlers.main.bot_start import edit_ls

from keyboards.inline.bus_stops import ikb_menu_bus_stops
from keyboards.inline.inline_kb_default import ikb_default
from states.regist import TimeRegistrate, Regist

from utils.db_api import quick_commands as commands
from utils.db_api.quick_commands import update_code_bus_stop, select_bus_stop_by_id
from utils.localization.i18n import MessageFormatter


@dp.callback_query_handler(text='change_code_bus_stop')
async def change_code_bus_stop_start(call: types.CallbackQuery):
    user = await commands.select_user(call.from_user.id)
    bus_stops = await commands.select_all_bus_stops(user)

    # Объединяем клавиатуры
    ikb = types.InlineKeyboardMarkup(row_width=2)
    ikb.inline_keyboard = ikb_menu_bus_stops(
        user,
        bus_stops,
        False, "change_code").inline_keyboard + ikb_default(user,
                                                            {'back_to_settings': 'back_to_settings',
                                                             'back_to_main_menu': 'back_to_main_menu'
                                                             }).inline_keyboard

    await edit_ls.edit_last_message(
        MessageFormatter(user.language).get_message({'setting_choose_bus_stop_change': 'bold'}),
        call, ikb
    )


@dp.callback_query_handler(text_startswith='change_code')
async def change_code_bus_stop(call: types.CallbackQuery, state: FSMContext):
    callback_data = call.data
    splitted_data = callback_data.split('_')
    Regist.change_code_bus_stop.stop_code = splitted_data[2]
    Regist.change_code_bus_stop.id_stop = splitted_data[3]

    user = await commands.select_user(call.from_user.id)
    asyncio.create_task(TimeRegistrate(state, call, user).state_timer())

    sent_message = await edit_ls.edit_last_message(
        MessageFormatter(user.language).get_message({'bus_stops_id_stop': 'none'}),
        call, None, 'HTML', True
    )
    Regist.change_code_bus_stop.message_id = sent_message.message_id  # Сохраняем message_id
    await Regist.change_code_bus_stop.set()


@dp.message_handler(state=Regist.change_code_bus_stop)
async def change_code_bus_stop_finish(message: types.Message, state: FSMContext):
    user = await commands.select_user(message.from_user.id)
    await state.update_data(stop_code=message.text)
    data = await state.get_data()
    stop_code = data.get('stop_code')
    id_stop = int(Regist.change_code_bus_stop.id_stop)
    bus_stop = await select_bus_stop_by_id(id_stop)
    await update_code_bus_stop(id_stop, int(stop_code))
    await bot.delete_message(message.from_user.id, message.message_id)
    await bot.delete_message(message.from_user.id, Regist.change_code_bus_stop.message_id)
    await edit_ls.edit_last_message(
        MessageFormatter(user.language).get_message({'bus_stops_finish_add_stop': 'none'},
                                                    {'name': bus_stop.name,
                                                     'id_stop': stop_code}),
        message, ikb_default(user,
                             {'back_to_settings': 'back_to_settings',
                              'back_to_main_menu': 'back_to_main_menu'
                              })
    )
    await state.finish()

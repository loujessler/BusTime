from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from bot.loader import dp, bot

from bot.handlers.main.bot_start import edit_ls

from bot.keyboards.inline.bus_stops import ikb_menu_bus_stops
from bot.keyboards.inline.inline_kb_default import ikb_default

from bot.states.regist import Regist

from bot.utils.cancel_state import cancel_func
from bot.utils.db_api import quick_commands as commands
from bot.utils.db_api.quick_commands import update_code_bus_stop, select_bus_stop_by_id
from bot.utils.localization.i18n import MessageFormatter


# Отмена при определенных состояниях
@dp.message_handler(Command('cancel'), state=Regist.change_code_bus_stop)
async def ignore_commands_in_state(message: types.Message, state: FSMContext):
    state_mapping = {
        'Regist:change_code_bus_stop': Regist.change_code_bus_stop,
    }
    format_dict = {'change_code_bus_stops_cancel': 'none'}
    buttons = {
        'back_to_settings': 'back_to_settings',
        'back_to_main_menu': 'back_to_main_menu',
    }
    user = message.conf.get('user')
    await cancel_func(message, user.language, state, state_mapping, format_dict, buttons)


@dp.callback_query_handler(text='change_code_bus_stop')
async def change_code_bus_stop_start(call: types.CallbackQuery):
    user = call.conf.get('user')
    bus_stops = await commands.select_all_bus_stops(user)

    # Объединяем клавиатуры
    ikb = types.InlineKeyboardMarkup(row_width=2)
    ikb.inline_keyboard = ikb_menu_bus_stops(
        user,
        bus_stops,
        False, "change_code").inline_keyboard + ikb_default(user.language,
                                                            {'back_to_settings': 'back_to_settings',
                                                             'back_to_main_menu': 'back_to_main_menu'
                                                             }).inline_keyboard

    await edit_ls.edit_last_message(
        MessageFormatter(user.language).get_message({'setting_choose_bus_stop_change': 'bold'}),
        call, ikb
    )


@dp.callback_query_handler(text_startswith='change_code')
async def change_code_bus_stop(call: types.CallbackQuery):
    callback_data = call.data
    splitted_data = callback_data.split('_')
    Regist.change_code_bus_stop.stop_code = splitted_data[2]
    Regist.change_code_bus_stop.id_stop = splitted_data[3]

    user = call.conf.get('user')

    sent_message = await edit_ls.edit_last_message(
        MessageFormatter(user.language).get_message(format_dict={'bus_stops_id_stop': 'none',
                                                                 'click_for_cancel': 'italic'},
                                                    line_breaks=2),
        call, None, 'HTML', True
    )
    Regist.change_code_bus_stop.message_id = sent_message.message_id  # Сохраняем message_id
    await Regist.change_code_bus_stop.set()


@dp.message_handler(state=Regist.change_code_bus_stop)
async def change_code_bus_stop_finish(message: types.Message, state: FSMContext):
    user = message.conf.get('user')
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
        message, ikb_default(user.language,
                             {'back_to_settings': 'back_to_settings',
                              'back_to_main_menu': 'back_to_main_menu'
                              })
    )
    await state.finish()

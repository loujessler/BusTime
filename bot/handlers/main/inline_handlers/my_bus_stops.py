from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Regexp

from bot.loader import dp, bot

from bot.keyboards.inline.bus_stops import ikb_menu_bus_stops

from bot.states.regist import Regist
from bot.handlers.main.utils.warnings.errors_bus_stop_input import error_regexp, error_bus_stop
from bot.handlers.main.utils.cancel import cancel_func
from bot.handlers.main.utils.my_bus_stops import my_bus_stops

from bot.utils.db_api import quick_commands as commands
from bot.utils.localization.i18n import MessageFormatter

from bot.handlers.main.bot_start import edit_ls


@dp.callback_query_handler(text='my_bus_stops')
async def callback_my_bus_stops(call: types.CallbackQuery):
    await my_bus_stops(call)


# Отмена при определенных состояниях
@dp.message_handler(Command('cancel'), state=[Regist.name_bus_stops_state, Regist.id_bus_stops_state])
async def cancel_state_bus_stops(message: types.Message, state: FSMContext):
    state_mapping = {
        'Regist:name_bus_stops_state': Regist.name_bus_stops_state,
        'Regist:id_bus_stops_state': Regist.id_bus_stops_state,
    }
    format_dict = {'bus_stops_finish_cancel': 'none'}
    user = message.conf.get('user')
    await cancel_func(message, user.language, state, state_mapping, format_dict)


# Игнорирование состояния при определенных состояниях
@dp.message_handler(Regexp("^/"), state=[Regist.name_bus_stops_state, Regist.id_bus_stops_state])
async def ignore_commands_in_state(message: types.Message):
    await message.delete()


@dp.message_handler(Regexp(r'^[^\d]+$'), state=Regist.id_bus_stops_state)
async def add_bus_stop_error_regexp(message: types.Message):
    await error_regexp(message)


@dp.message_handler(is_bus_stop=False, state=Regist.id_bus_stops_state)
async def add_bus_stop_error_bus_stop(message: types.Message):
    await error_bus_stop(message)


@dp.callback_query_handler(text_startswith='add_new_bus_stop')
async def set_name_bus_stops(call: types.CallbackQuery):
    user = call.conf.get('user')
    # Получаем данные из обратного вызова
    splitted_data = call.data.split('_')
    if len(splitted_data) > 4:
        name = splitted_data[4]
        id_stop = int(splitted_data[5])
        await commands.add_bus_stop(user, name=name, id_stop=id_stop)
        await bot.delete_message(call.message.chat.id, splitted_data[6])
        bus_stops = await commands.select_all_bus_stops(user)
        msg_f = MessageFormatter(user.language)
        if bus_stops:
            await edit_ls.edit_last_message(
                msg_f.get_message(format_dict={'bus_stops_finish_add_stop': 'none'},
                                  format_args={'name': name, 'id_stop': id_stop}),
                call, ikb_menu_bus_stops(user, bus_stops)
            )
        else:
            await edit_ls.edit_last_message(
                msg_f.get_message({'bus_stops_finish_cancel': 'none'}),
                call
            )
    else:
        sent_message = await edit_ls.edit_last_message(
            MessageFormatter(user.language).get_message(format_dict={'bus_stops_name': 'none',
                                                                     'click_for_cancel': 'italic'},
                                                        line_breaks=2),
            call, None, 'HTML', True
        )
        Regist.name_bus_stops_state.message_id = sent_message.message_id  # Сохраняем message_id
        await Regist.name_bus_stops_state.set()


@dp.message_handler(state=Regist.name_bus_stops_state)
async def number_bus_stop(message: types.Message, state: FSMContext):
    user = message.conf.get('user')
    await state.update_data(name=message.text)

    for msg_id in [message.message_id, Regist.name_bus_stops_state.message_id]:
        await bot.delete_message(message.from_user.id, msg_id)

    sent_message = await edit_ls.edit_last_message(
        MessageFormatter(user.language).get_message(format_dict={'bus_stops_id_stop': 'none',
                                                                 'click_for_cancel': 'italic'},
                                                    line_breaks=2),
        message, None, 'HTML', True
    )
    Regist.id_bus_stops_state.message_id = sent_message.message_id
    await Regist.id_bus_stops_state.set()


@dp.message_handler(is_bus_stop=True, state=Regist.id_bus_stops_state)
async def create_fav_bus_stop(message: types.Message, state: FSMContext):
    user = message.conf.get('user')
    id_stop = int(message.text)
    await state.update_data(id_stop=id_stop)
    data = await state.get_data()
    name = data.get('name')

    for msg_id in [message.message_id, Regist.id_bus_stops_state.message_id]:
        await bot.delete_message(message.from_user.id, msg_id)

    await commands.add_bus_stop(user, name=name, id_stop=id_stop)
    bus_stops = await commands.select_all_bus_stops(user)
    msg_f = MessageFormatter(user.language)
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

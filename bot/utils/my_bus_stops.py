from bot.states.regist import Regist

from bot.keyboards.inline.bus_stops import ikb_menu_bus_stops

from bot.utils.db_api import quick_commands as commands

from bot.handlers.main.bot_start import edit_ls
from bot.utils.localization.i18n import MessageFormatter


async def my_bus_stops(aio_type):
    user = aio_type.conf.get('user')
    if user:
        bus_stops = await commands.select_all_bus_stops(user)
        if bus_stops:
            await edit_ls.edit_last_message(
                MessageFormatter(user.language).get_message({'bus_stops_choose_bus_stop': 'none'}),
                aio_type, ikb_menu_bus_stops(user, bus_stops)
            )
        else:
            sent_message = await edit_ls.edit_last_message(
                MessageFormatter(user.language).get_message(format_dict={'bus_stops_no_bus_stops': 'none',
                                                                         'click_for_cancel': 'italic'},
                                                            line_breaks=2),
                aio_type, None, 'HTML', True
            )
            Regist.name_bus_stops_state.message_id = sent_message.message_id  # Сохраняем message_id
            await Regist.name_bus_stops_state.set()

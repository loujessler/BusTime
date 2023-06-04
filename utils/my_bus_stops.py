from states.regist import Regist

from keyboards.inline.bus_stops import ikb_menu_bus_stops

from utils.additional import return_msg_aio_type
from utils.db_api import quick_commands as commands

from handlers.main.bot_start import edit_ls
from utils.i18n import MessageFormatter


async def my_bus_stops(aio_type):
    message = return_msg_aio_type(aio_type)
    user = await commands.select_user(message.chat.id)
    if user:
        bus_stops = await commands.select_all_bus_stops(user)
        if bus_stops:
            # for bus_stop in bus_stops:
            #     print(f"Bus Stop: {bus_stop.name}, ID: {bus_stop.id_stop}")
            # await edit_ls.edit_last_message(
            #     BusStopsMSG(user).choose_bus_stop[user.language],
            #     message, ikb=ikb_menu_bus_stops(bus_stops)
            # )
            await edit_ls.edit_last_message(
                MessageFormatter(user).get_message({'bus_stops_choose_bus_stop': 'none'}),
                aio_type, ikb_menu_bus_stops(user, bus_stops)
            )
        else:
            await edit_ls.edit_last_message(
                MessageFormatter(user).get_message({'bus_stops_no_bus_stops': 'none'}),
                aio_type
            )
            await Regist.name_bus_stops_state.set()

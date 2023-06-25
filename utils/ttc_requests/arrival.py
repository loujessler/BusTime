import httpx

from loader import bot

from keyboards.inline.inline_kb_default import ikb_default

from utils.additional import return_msg_aio_type
from utils.data_utils.json_data import load_stops_data
from utils.edit_last_message import EditLastMessage
from utils.db_api import quick_commands as commands
from utils.localization.i18n import MessageFormatter

from data.messages.arrival_messages import ArrivalMessages

edit_ls = EditLastMessage(bot)


async def arrival(code_bus_stop, aio_type):
    message = await return_msg_aio_type(aio_type)
    try:
        await message.delete()
    except:
        pass
    user = await commands.select_user(aio_type.from_user.id)
    if str(code_bus_stop) not in load_stops_data('code'):
        await edit_ls.edit_last_message(
            MessageFormatter(user.language).get_message({'arrival_bus_stop_not_exists': 'bold'}),
            aio_type,
            ikb_default(user, {
                'back_to_main_menu': 'back_to_main_menu',
            })
        )
    else:
        chat_id = message.chat.id
        url = f'http://transfer.ttc.com.ge:8080/otp/routers/ttc/stopArrivalTimes?stopId={code_bus_stop}'

        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                response = await client.get(url)
                response.raise_for_status()  # This will raise an exception for 4xx and 5xx status codes

            json_data = response.json()

            arrival_time_key = 'ArrivalTime'

            if arrival_time_key not in json_data:
                await bot.send_message(chat_id, f'{arrival_time_key} key not found in JSON data')
                return

            arrival_times = json_data[arrival_time_key]
            num_arrival_times = len(arrival_times)
            msg = ArrivalMessages(user, arrival_times, code_bus_stop)

            if num_arrival_times:
                await edit_ls.edit_last_message(
                    msg.bus_arrival_times(),
                    aio_type,
                    ikb_default(user, {
                        'refresh': f'stop_{code_bus_stop}',
                        'notification': 'notification',
                        'back_to_main_menu': 'back_to_main_menu',
                    })
                )
            else:
                await edit_ls.edit_last_message(
                    msg.bus_arrival_not(),
                    aio_type,
                    ikb_default(user, {
                        'refresh': f'stop_{code_bus_stop}',
                        'back_to_main_menu': 'back_to_main_menu',
                    })
                )

        except httpx.HTTPStatusError as e:
            await bot.send_message(chat_id, f'Error while executing request: {e}')
        except httpx.ReadTimeout:
            await bot.send_message(chat_id, "The request to the server has timed out. Please try again later.")

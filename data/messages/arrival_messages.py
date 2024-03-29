from transliterate import translit

import aiogram.utils.markdown as fmt

from bot.handlers.main.utils.get_url_bot import get_bot_link
from bot.utils.additional import capitalize_words, ConvertNumber
from bot.utils.localization.i18n import MessageFormatter


class ArrivalMessages:
    def __init__(self, user, arrival_times, code_bus_stop):
        self.user = user
        self.arrival_times = arrival_times
        self.code_bus_stop = code_bus_stop

    async def bus_arrival_times(self):
        conv_numb = ConvertNumber('emoji_numbers')
        message = f"🚏 → {conv_numb.convert(self.code_bus_stop)}\n\n"
        for arrival_time in self.arrival_times:
            route_number = int(arrival_time['RouteNumber'])
            minutes = arrival_time['ArrivalTime']
            destination_name = arrival_time['DestinationStopName'] if self.user.language == 'ka' else \
                translit(arrival_time['DestinationStopName'], 'ka', reversed=True)
            sticker_time = '⚡️' if minutes <= 5 else '⏳'
            type_transport = '🚌' if route_number < 400 else '🚐'
            # Create arrival text with link
            bot_link = await get_bot_link()
            route_number = f"[{conv_numb.convert(route_number)}]({bot_link}?start=search_route_{route_number})"
            line_msg = MessageFormatter(self.user.language).get_message(
                {'arrival_bus_times': 'none'},
                {'route_number': route_number,
                 'type_transport': type_transport,
                 'minutes': minutes,
                 'sticker_time': sticker_time,
                 'destination_name': await capitalize_words(destination_name)}),
            message += line_msg[0] + "\n"
        return fmt.text(message)

    async def bus_arrival_not(self):
        return MessageFormatter(self.user.language).get_message({'arrival_bus_not': 'none'})

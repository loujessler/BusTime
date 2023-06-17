import aiogram.utils.markdown as fmt

from utils.additional import number_to_emoji
from utils.localization.i18n import MessageFormatter


class ArrivalMessages:
    def __init__(self, user, arrival_times, code_bus_stop):
        self.user = user
        self.arrival_times = arrival_times
        self.code_bus_stop = code_bus_stop

    def bus_arrival_times(self):
        message = f'🚏 → {number_to_emoji(self.code_bus_stop)}\n\n'
        for arrival_time in self.arrival_times:
            route_number = int(arrival_time['RouteNumber'])
            minutes = arrival_time['ArrivalTime']
            sticker_time = '⚡️' if minutes <= 5 else '⏳'
            type_transport = '🚌' if route_number < 400 else '🚐'
            line_msg = MessageFormatter(self.user.language).get_message({'arrival_bus_times': 'none'},
                                                                        {'route_number': number_to_emoji(route_number),
                                                                         'type_transport': type_transport,
                                                                         'minutes': minutes,
                                                                         'sticker_time': sticker_time}),
            message += line_msg[0] + "\n"
        return fmt.text(message)

    def bus_arrival_not(self):
        return MessageFormatter(self.user.language).get_message({'arrival_bus_not': 'none'})

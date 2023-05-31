import aiogram.utils.markdown as fmt
import requests

from utils.additional import number_to_emoji


class ArrivalMessages:
    def __init__(self, user, arrival_times, code_bus_stop):
        self.user = user
        self.arrival_times = arrival_times
        self.code_bus_stop = code_bus_stop

    def bus_arrival_times(self):
        message = f'🚏 → {number_to_emoji(self.code_bus_stop)}\n\n'
        for arrival_time in self.arrival_times:
            route_number = arrival_time['RouteNumber']
            minutes = arrival_time['ArrivalTime']
            destination_stop_name = arrival_time['DestinationStopName']
            # try:
            #     url = f'http://translate.google.ru/translate_a/t?client=x&text={destination_stop_name}&hl=en&sl=en&tl=ru'
            #     response = requests.get(url)
            #     print(response)
            # except Exception as e:
            #     print(f'Error: {e}')

            if minutes > 5:
                sticker_time = '⏳'
            else:
                sticker_time = '⚡️'
            if self.user.language == 'ru':
                line_msg = f'{sticker_time} {number_to_emoji(route_number)} → {minutes} мин \n'
            elif self.user.language == 'en':
                line_msg = f'{sticker_time} {number_to_emoji(route_number)} → {minutes} min \n'
            else:
                line_msg = ""
            message += line_msg
        return fmt.text(message)

    def bus_arrival_not(self):
        message = f''
        if self.user.language == 'ru':
            line_msg = f'В ближайшее время 🚌 не ожидается или такой 🚏 не существует\n'
        elif self.user.language == 'en':
            line_msg = f'🚌 is not expected in the near future or there is no such 🚏\n'
        else:
            line_msg = ""
        message += line_msg
        return fmt.text(message)

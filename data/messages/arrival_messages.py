import aiogram.utils.markdown as fmt

from utils.additional import number_to_emoji
from utils.i18n import MessageFormatter


class ArrivalMessages:
    messages = {
        'bus_arrival_times': {
            'ru': '{sticker_time} {route_number} → {minutes} мин',
            'en': '{sticker_time} {route_number} → {minutes} min',
            'ka': '{sticker_time} {route_number} → {minutes} წუთ',
        },
        'bus_arrival_not': {
            'ru': 'В ближайшее время 🚌 не ожидается или такой 🚏 не существует',
            'en': 'No 🚌 is expected in the near future or such a 🚏 does not exist',
            'ka': 'ახლოს 🚌 არ ელოდება ან ასეთი 🚏 არ არსებობს',
        }
    }

    def __init__(self, user, arrival_times, code_bus_stop):
        self.user = user
        self.arrival_times = arrival_times
        self.code_bus_stop = code_bus_stop

    def bus_arrival_times(self):
        message = f'🚏 → {number_to_emoji(self.code_bus_stop)}\n\n'
        for arrival_time in self.arrival_times:
            route_number = number_to_emoji(arrival_time['RouteNumber'])
            minutes = arrival_time['ArrivalTime']
            sticker_time = '⚡️' if minutes <= 5 else '⏳'
            # line_msg = self.messages['bus_arrival_times'][self.user.language].format(sticker_time=sticker_time,
            #                                                                          route_number=route_number,
            #                                                                          minutes=minutes)
            line_msg = MessageFormatter(self.user).get_message({'arrival_bus_times': 'none'},
                                                               {'route_number': route_number,
                                                                'minutes': minutes,
                                                                'sticker_time': sticker_time}),
            message += line_msg + "\n"
        return fmt.text(message)

    def bus_arrival_not(self):
        return MessageFormatter(self.user).get_message({'arrival_bus_not': 'none'})

# import aiogram.utils.markdown as fmt
#
# from utils.additional import number_to_emoji
#
#
# class ArrivalMessages:
#     def __init__(self, user, arrival_times, code_bus_stop):
#         self.user = user
#         self.arrival_times = arrival_times
#         self.code_bus_stop = code_bus_stop
#
#     def bus_arrival_times(self):
#         message = f'🚏 → {number_to_emoji(self.code_bus_stop)}\n\n'
#         for arrival_time in self.arrival_times:
#             route_number = arrival_time['RouteNumber']
#             minutes = arrival_time['ArrivalTime']
#             destination_stop_name = arrival_time['DestinationStopName']
#             # try:
#             #     url = f'http://translate.google.ru/translate_a/t?client=x&text={destination_stop_name}&hl=en&sl=en&tl=ru'
#             #     response = requests.get(url)
#             #     print(response)
#             # except Exception as e:
#             #     print(f'Error: {e}')
#
#             if minutes > 5:
#                 sticker_time = '⏳'
#             else:
#                 sticker_time = '⚡️'
#             if self.user.language == 'ru':
#                 line_msg = f'{sticker_time} {number_to_emoji(route_number)} → {minutes} мин \n'
#             elif self.user.language == 'en':
#                 line_msg = f'{sticker_time} {number_to_emoji(route_number)} → {minutes} min \n'
#             else:
#                 line_msg = ""
#             message += line_msg
#         return fmt.text(message)
#
#     def bus_arrival_not(self):
#         message = f''
#         if self.user.language == 'ru':
#             line_msg = f'В ближайшее время 🚌 не ожидается или такой 🚏 не существует\n'
#         elif self.user.language == 'en':
#             line_msg = f'🚌 is not expected in the near future or there is no such 🚏\n'
#         else:
#             line_msg = ""
#         message += line_msg
#         return fmt.text(message)

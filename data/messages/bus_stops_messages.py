import aiogram.utils.markdown as fmt


class BusStopsMSG:
    def __init__(self, user):
        self.user = user

    no_bus_stops = {
        'ru': '🚫 У вас ещё нет избранных остановок\n\n🔠 Введите имя остановки:',
        'en': "🚫 You don't have any favorite stops yet\n\n🔠 Enter the name of the stop:",
        'ka': '🚫 თქვენ ჯერ არ გაქვთ ფავორიტი გაჩერების ადგილები\n\n🔠 შეიყვანეთ გაჩერების ადგილის სახელი:'
    }

    name = {
        'ru': '🔠 Введите имя остановки:',
        'en': '🔠 Enter the name of the stop:',
        'ka': '🔠 შეიყვანეთ გაჩერების ადგილის სახელი:'
    }

    id_stop = {
        'ru': '🆔 Введите ID остановки:',
        'en': '🆔 Enter the ID of the stop:',
        'ka': '🆔 შეიყვანეთ გაჩერების ადგილის ID:'
    }

    choose_bus_stop = {
        'ru': '🔍 Выберите избранную остановку',
        'en': '🔍 Select a favorite stop',
        'ka': '🔍 აირჩიეთ ფავორიტი გაჩერების ადგილი'
    }

    def finish_add_stop(self, name, id_stop):
        message = {
            'ru': f'✅ Сохранена остановка: {name} - {id_stop}',
            'en': f'✅ Stop saved: {name} - {id_stop}',
            'ka': f'✅ გაჩერების ადგილი შენახულია: {name} - {id_stop}'
        }
        return message[self.user.language]

    def get_message(self, message_name):
        return fmt.text(fmt.hbold(self.__class__.__dict__[message_name][self.user.language]))


# import aiogram.utils.markdown as fmt
# from utils.db_api import quick_commands as commands
#
#
# class BusStopsMSG:
#     no_bus_stops = {
#         'ru': fmt.text(
#             fmt.hbold('У вас ещё нет избранных остановок\n\n'),
#             'Введите имя остановки:'
#         ),
#         'en': fmt.text(
#             fmt.hbold('✨ You have been given a Tron wallet\n\n'),
#             '💰 Your wallet: \n\n'
#         ),
#     }
#
#     name = {
#         'ru': fmt.text(
#             'Введите имя остановки:'
#         ),
#         'en': fmt.text(
#             fmt.hbold('✨ You have been given a Tron wallet\n\n'),
#             '💰 Your wallet: \n\n'
#         ),
#     }
#
#     id_stop = {
#         'ru': fmt.text(
#             'Введите ID остановки:'
#         ),
#         'en': fmt.text(
#             fmt.hbold('✨ You have been given a Tron wallet\n\n'),
#             '💰 Your wallet: \n\n'
#         ),
#     }
#
#     choose_bus_stop = {
#         'ru': fmt.text(
#             'Выберете избранную остановку'
#         ),
#         'en': fmt.text(
#             fmt.hbold('✨ You have been given a Tron wallet\n\n'),
#             '💰 Your wallet: \n\n'
#         ),
#     }
#
#     def __init__(self, user):
#         self.user = user
#
#     def finish_add_stop(self, name, id_stop):
#         message = {
#             'ru': fmt.text(
#                 f'Сохранена остановка: {name} - {id_stop}'
#             ),
#             'en': fmt.text(
#                 fmt.hbold('✨ You have been given a Tron wallet\n\n'),
#                 '💰 Your wallet: \n\n'
#             ),
#         }
#         return message[self.user.language]

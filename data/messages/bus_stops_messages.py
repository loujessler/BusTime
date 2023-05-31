import aiogram.utils.markdown as fmt
from utils.db_api import quick_commands as commands


class BusStopsMSG:
    no_bus_stops = {
        'ru': fmt.text(
            fmt.hbold('У вас ещё нет избранных остановок\n\n'),
            'Введите имя остановки:'
        ),
        'en': fmt.text(
            fmt.hbold('✨ You have been given a Tron wallet\n\n'),
            '💰 Your wallet: \n\n'
        ),
    }

    name = {
        'ru': fmt.text(
            'Введите имя остановки:'
        ),
        'en': fmt.text(
            fmt.hbold('✨ You have been given a Tron wallet\n\n'),
            '💰 Your wallet: \n\n'
        ),
    }

    id_stop = {
        'ru': fmt.text(
            'Введите ID остановки:'
        ),
        'en': fmt.text(
            fmt.hbold('✨ You have been given a Tron wallet\n\n'),
            '💰 Your wallet: \n\n'
        ),
    }

    choose_bus_stop = {
        'ru': fmt.text(
            'Выберете избранную остановку'
        ),
        'en': fmt.text(
            fmt.hbold('✨ You have been given a Tron wallet\n\n'),
            '💰 Your wallet: \n\n'
        ),
    }

    def __init__(self, user):
        self.user = user

    def finish_add_stop(self, name, id_stop):
        message = {
            'ru': fmt.text(
                f'Сохранена остановка: {name} - {id_stop}'
            ),
            'en': fmt.text(
                fmt.hbold('✨ You have been given a Tron wallet\n\n'),
                '💰 Your wallet: \n\n'
            ),
        }
        return message[self.user.language]

    # def new_bus_stop(self, msg_name):
    #     message = {
    #         'no_bus_stops': {
    #             'ru': fmt.text(
    #                 fmt.hbold('У вас ещё нет избранных остановок\n\n'),
    #                 'Введите имя остановки:'
    #             ),
    #             'en': fmt.text(
    #                 fmt.hbold('✨ You have been given a Tron wallet\n\n'),
    #                 '💰 Your wallet: \n\n'
    #             ),
    #         },
    #         'id_stop': {
    #             'ru': fmt.text(
    #                 'Введите ID остановки:'
    #             ),
    #             'en': fmt.text(
    #                 fmt.hbold('✨ You have been given a Tron wallet\n\n'),
    #                 '💰 Your wallet: \n\n'
    #             ),
    #         }
    #
    #     }
    #     return message[msg_name][self.user.language]

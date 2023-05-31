import aiogram.utils.markdown as fmt

from data.languages import languages


class Messages:
    def __init__(self, user):
        self.user = user

    def menu_msg(self):
        menu = {
            'ru': fmt.text(
                fmt.hbold('⚙️ Настройки\n\n'),
                f'Язык: {languages[self.user.language]}'
            ),
            'en': fmt.text(
                fmt.hbold('⚙️ Settings\n\n'),
                f'Language: {languages[self.user.language]}'
            )
        }
        return menu

    # Change Language
    change_language = {
        'ru': fmt.text(
            fmt.hbold('Изменить язык')
        ),
        'en': fmt.text(
            fmt.hbold('Change language')
        )
    }
    change_language_done = {
        'ru': fmt.text(
            fmt.hbold('Язык успешно изменен')
        ),
        'en': fmt.text(
            fmt.hbold('Language changed successfully')
        )
    }

    # _______________________________________Remove stop
    choose_bus_stop = {
        'ru': fmt.text(
            fmt.hbold('Выберете остановку, которую хотите удалить')
        ),
        'en': fmt.text(
            fmt.hbold('Select the stop you want to delete')
        )
    }

    delete_stop_true = {
        'ru': fmt.text(
            fmt.hbold('Остановка успешно удалена')
        ),
        'en': fmt.text(
            fmt.hbold('Stop deleted successfully')
        )
    }

    delete_stop_false = {
        'ru': fmt.text(
            fmt.hbold('Остановка не удалена. Повторите попытку')
        ),
        'en': fmt.text(
            fmt.hbold("The stop hasn't been removed. Try again")
        )
    }


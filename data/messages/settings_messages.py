import aiogram.utils.markdown as fmt

from data.languages import languages


class Messages:
    def __init__(self, user):
        self.user = user

    def menu_msg(self):
        menu = {
            'ru': fmt.text(
                fmt.hbold('🔧⚙️ Настройки\n\n'),
                f'🌐 Язык: {languages[self.user.language]}'
            ),
            'en': fmt.text(
                fmt.hbold('🔧⚙️ Settings\n\n'),
                f'🌐 Language: {languages[self.user.language]}'
            ),
            'ka': fmt.text(
                fmt.hbold('🔧⚙️ პარამეტრები\n\n'),
                f'🌐 ენა: {languages[self.user.language]}'
            )
        }
        return menu[self.user.language]

    # Change Language
    change_language = {
        'ru': fmt.text(fmt.hbold('🌐 Изменить язык')),
        'en': fmt.text(fmt.hbold('🌐 Change language')),
        'ka': fmt.text(fmt.hbold('🌐 ენის შეცვლა')),
    }

    def get_change_language(self):
        return self.change_language[self.user.language]

    change_language_done = {
        'ru': fmt.text(fmt.hbold('🔄 Язык успешно изменен')),
        'en': fmt.text(fmt.hbold('🔄 Language changed successfully')),
        'ka': fmt.text(fmt.hbold('🔄 ენა შეიცვალა წარმატებით')),
    }

    def get_change_language_done(self):
        return self.change_language_done[self.user.language]

    # Remove stop
    choose_bus_stop = {
        'ru': fmt.text(fmt.hbold('🚏 Выберите остановку, которую хотите удалить')),
        'en': fmt.text(fmt.hbold('🚏 Select the stop you want to delete')),
        'ka': fmt.text(fmt.hbold('🚏 აირჩიეთ გაჩერების ადგილი, რომელსაც გსურთ წაშლა')),
    }

    def get_choose_bus_stop(self):
        return self.choose_bus_stop[self.user.language]

    delete_stop_true = {
        'ru': fmt.text(fmt.hbold('✅ Остановка успешно удалена')),
        'en': fmt.text(fmt.hbold('✅ Stop deleted successfully')),
        'ka': fmt.text(fmt.hbold('✅ გაჩერების ადგილი წაიშალა წარმატებით')),
    }

    def get_delete_stop_true(self):
        return self.delete_stop_true[self.user.language]

    delete_stop_false = {
        'ru': fmt.text(fmt.hbold('❌ Остановка не удалена. Повторите попытку')),
        'en': fmt.text(fmt.hbold("❌ The stop hasn't been removed. Try again")),
        'ka': fmt.text(fmt.hbold("❌ გაჩერების ადგილი არ არის წაშლილი. სცადეთ თავიდან")),
    }

    def get_delete_stop_false(self):
        return self.delete_stop_false[self.user.language]

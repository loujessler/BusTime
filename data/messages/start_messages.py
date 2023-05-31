import aiogram.utils.markdown as fmt
from utils.db_api import quick_commands as commands


class Messages:
    def __init__(self, user):
        self.user = user

    @staticmethod
    def language_mes(aio_type):
        text = fmt.text(
            f'✌️ Hi, {aio_type.from_user.first_name}.\n',
            fmt.hbold('🏳️ Choose your language: ')
        )
        return text

    def finish_registration(self):
        message = {
            'ru': fmt.text(
                fmt.hbold('✨ Вы попали на главное меню бота\n\n'),
                'Здесь вы можете указать ID вашей остановки и узнать расписание автобусов.'
            ),
            'en': fmt.text(
                fmt.hbold('✨ You have been given a Tron wallet\n\n'),
                '💰 Your wallet: \n\n',
                '\n\n',
                '🔐 Your private key: \n',
                '\n\n📝 Be sure to save your private key to restore your wallet!\n\n',
                'Start from the main menu ➡️ /menu'
            ),
        }
        return message[self.user.language]

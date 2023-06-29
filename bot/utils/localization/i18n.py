from loguru import logger
import aiogram.utils.markdown as fmt
from babel.support import Translations

from data import config


class MessageFormatter:
    # Словарь соответствия стилей функциям форматирования
    FORMAT_FUNCTIONS = {
        'bold': fmt.hbold,
        'italic': fmt.hitalic,
        'link': fmt.hlink,
        'none': str,  # Стиль без форматирования
    }

    def __init__(self, language: str, domain=config.I18N_DOMAIN):
        self.language = language
        self.domain = domain

    def get_translations(self) -> Translations:
        return Translations.load(config.LOCALES_DIR, [self.language], self.domain)

    def get_message(self, format_dict, format_args=None, line_breaks=0) -> str:
        translation = self.get_translations()
        messages = []

        for message_id, format_name in format_dict.items():
            # Получаем функцию форматирования из словаря по имени стиля
            format_func = self.FORMAT_FUNCTIONS.get(format_name)

            message = translation.gettext(message_id)

            # Если есть аргументы для форматирования, вставляем их в сообщение
            if format_args is not None:
                message = message.format(**format_args)

            # Если нет перевода для message_id
            if message == message_id:
                logger.warning(f"Warning: no translation for {message_id} in {self.language}")
                message = format_func(message_id)  # Используем идентификатор сообщения вместо перевода
            else:
                if format_name == 'link':
                    url = translation.gettext(message_id + '_link')
                    message = format_func(message, url)
                else:
                    message = format_func(message)

            messages.append(message)

        return ('\n' * line_breaks).join(messages)

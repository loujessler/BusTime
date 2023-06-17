import aiogram.utils.markdown as fmt
from babel.support import Translations
from data import config


class MessageFormatter:
    # Словарь соответствия стилей функциям форматирования
    FORMAT_FUNCTIONS = {
        'bold': fmt.hbold,
        'italic': fmt.hitalic,
        'none': lambda text: text,  # Стиль без форматирования
        # Добавьте здесь другие стили по мере необходимости
    }

    def __init__(self, language):
        self.language = language

    def get_translations(self, domain):
        return Translations.load(config.LOCALES_DIR, [self.language], domain)

    def get_message(self, format_dict, format_args=None, line_breaks=0, domain=config.I18N_DOMAIN):
        translation = self.get_translations(domain)
        messages = []

        for message_id, format_name in format_dict.items():
            # Получаем функцию форматирования из словаря по имени стиля
            format_func = self.FORMAT_FUNCTIONS.get(format_name, lambda text: text)

            message = translation.gettext(message_id)

            # Если есть аргументы для форматирования, вставляем их в сообщение
            if format_args is not None:
                message = message.format(**format_args)

            # Если нет перевода для message_id
            if message == message_id:
                print(f"Warning: no translation for {message_id} in {self.language}")
                message = format_func(message_id)  # Используем идентификатор сообщения вместо перевода
            else:
                message = format_func(message)

            messages.append(message)

        return ('\n' * line_breaks).join(messages)

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.utils.localization.i18n import MessageFormatter

# texts = ['back_to_settings', 'back_to_main_menu']


def ikb_default(language: str, buttons: dict = None, domain: str = 'keyboards'):
    if buttons is None:
        buttons = {
            'back_to_main_menu': 'back_to_main_menu',
        }
    ikb = InlineKeyboardMarkup(row_width=1)
    for name, callback_data in buttons.items():
        ikb.add(InlineKeyboardButton(text=MessageFormatter(language, domain).get_message(
            {name: 'none'}, None, 0),
            callback_data=callback_data))
    return ikb

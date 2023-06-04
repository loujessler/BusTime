from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.i18n import MessageFormatter


texts = ['back_to_settings', 'back']


def ikb_back_to_settings(user):
    ikb = InlineKeyboardMarkup(row_width=1)
    for callback_data in texts:
        ikb.add(InlineKeyboardButton(text=MessageFormatter(user).get_message(
                                           {callback_data: 'none'}, None, 0, 'keyboards'),
                                     callback_data=callback_data))
    return ikb

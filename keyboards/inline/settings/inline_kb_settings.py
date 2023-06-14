from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.i18n import MessageFormatter


texts = ['change_language', 'delete_bus_stop', 'back']


def ikb_menu_settings(user):
    ikb = InlineKeyboardMarkup(row_width=1)
    for callback_data in texts:
        ikb.add(InlineKeyboardButton(text=MessageFormatter(user.language).get_message(
                                           {callback_data: 'none'}, None, 0, 'keyboards'),
                                     callback_data=callback_data))
    return ikb

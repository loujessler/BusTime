from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.i18n import MessageFormatter


# texts = ['back_to_settings', 'back_to_main_menu']


def ikb_default(user, texts=None):
    if texts is None:
        texts = ['back_to_main_menu']
    ikb = InlineKeyboardMarkup(row_width=1)
    for callback_data in texts:
        ikb.add(InlineKeyboardButton(text=MessageFormatter(user.language).get_message(
                                           {callback_data: 'none'}, None, 0, 'keyboards'),
                                     callback_data=callback_data))
    return ikb

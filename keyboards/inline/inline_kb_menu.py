from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.i18n import MessageFormatter


def ikb_menu(user):
    ikb = InlineKeyboardMarkup(row_width=2,
                               inline_keyboard=[
                                   [
                                       InlineKeyboardButton(text=MessageFormatter(user.language).get_message(
                                           {'bus_stops': 'none'}, None, 0, 'keyboards'),
                                           callback_data='my_bus_stops'),
                                   ],
                                   [
                                       InlineKeyboardButton(text=MessageFormatter(user.language).get_message(
                                           {'settings': 'none'}, None, 0, 'keyboards'),
                                                            callback_data='my settings'),
                                   ],
                               ])
    return ikb

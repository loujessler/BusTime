from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.utils.localization.i18n import MessageFormatter


def ikb_menu(user):
    formatter = MessageFormatter(user.language, 'keyboards')
    ikb = InlineKeyboardMarkup(row_width=2,
                               inline_keyboard=[
                                   [
                                       InlineKeyboardButton(text=formatter.get_message(
                                           {'bus_stops': 'none'}, None, 0),
                                           callback_data='my_bus_stops'),
                                   ],
                                   [
                                       InlineKeyboardButton(text=formatter.get_message(
                                           {'search_bus_stops': 'none'}, None, 0),
                                           callback_data='search_bus_stops'),
                                   ],
                                   [
                                       InlineKeyboardButton(text=formatter.get_message(
                                           {'settings': 'none'}, None, 0),
                                                            callback_data='my settings'),
                                   ],
                               ])
    return ikb

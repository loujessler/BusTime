from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

texts = {
    'bus_stops': {
        'ru': '🚏 Мои остановки',
        'en': '🚏 My bus stops',
        'ka': '🚏 ჩემი გაჩერებული გაჩერება'
    },
    'settings': {
        'ru': '⚙️ Настройки',
        'en': '⚙️ Settings',
        'ka': '⚙️ პარამეტრები'
    },
}


def ikb_menu(user):
    ikb = InlineKeyboardMarkup(row_width=2,
                               inline_keyboard=[
                                   [
                                       InlineKeyboardButton(text=texts['bus_stops'][user.language],
                                                            callback_data='my_bus_stops'),
                                   ],
                                   [
                                       InlineKeyboardButton(text=texts['settings'][user.language],
                                                            callback_data='my settings'),
                                   ],
                               ])
    return ikb

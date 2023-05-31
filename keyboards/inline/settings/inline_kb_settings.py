from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

texts = {
    'language': {
        'ru': 'Изменить язык',
        'en': 'Change language'
    },
    'delete_bus_stop': {
        'ru': 'Удалить остановку 🚏',
        'en': 'Remove stop 🚏'
    },
    'back': {
        'ru': '🔙 Назад',
        'en': '🔙 Back'
    },
}


def ikb_menu_settings(user):
    ikb = InlineKeyboardMarkup(row_width=1,
                               inline_keyboard=[
                                   [
                                       InlineKeyboardButton(text=texts['language'][user.language],
                                                            callback_data='change_language')
                                   ], [
                                       InlineKeyboardButton(text=texts['delete_bus_stop'][user.language],
                                                            callback_data='delete_bus_stop')
                                   ], [
                                       InlineKeyboardButton(text=texts['back'][user.language],
                                                            callback_data='back')
                                   ],
                               ]
                               )
    return ikb

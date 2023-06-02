from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

texts = {
    'change_language': {
        'ru': 'Изменить язык',
        'en': 'Change language',
        'ka': 'ენის შეცვლა'
    },
    'delete_bus_stop': {
        'ru': '🚏 Удалить остановку',
        'en': '🚏 Remove stop',
        'ka': '🚏 გამოჩენის წაშლა'
    },
    'back': {
        'ru': '🔙 Назад',
        'en': '🔙 Back',
        'ka': '🔙 უკან'
    },
}


def ikb_menu_settings(user):
    ikb = InlineKeyboardMarkup(row_width=1)
    for callback_data in texts.keys():
        ikb.add(InlineKeyboardButton(text=texts[callback_data][user.language],
                                     callback_data=callback_data))
    return ikb

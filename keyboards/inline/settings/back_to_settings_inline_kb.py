from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

texts = {
    'back_to_settings': {
        'ru': '🔙 Назад в настройки',
        'en': '🔙 Back to settings',
        'ka': '🔙 დაბრუნება პარამეტრებში'
    },
    'back': {
        'ru': '🔝 В главное меню',
        'en': '🔝 Main menu',
        'ka': '🔝 მთავარი მენიუ'
    },
}


def ikb_back_to_settings(user):
    ikb = InlineKeyboardMarkup(row_width=1)
    for callback_data in texts.keys():
        ikb.add(InlineKeyboardButton(text=texts[callback_data][user.language],
                                     callback_data=callback_data))
    return ikb

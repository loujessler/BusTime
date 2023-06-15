from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.i18n import MessageFormatter


def make_keyboard(user, minutes, seconds):
    keyboard = InlineKeyboardMarkup()
    msg = MessageFormatter(user.language)
    keyboard.row(
        InlineKeyboardButton('<', callback_data=f"dec_minutes:{minutes}:{seconds}"),
        InlineKeyboardButton(f"{minutes} {msg.get_message({'minutes': 'none'}, None, 0, 'keyboards')}",
                             callback_data=f"nothing"),
        InlineKeyboardButton('>', callback_data=f"inc_minutes:{minutes}:{seconds}"),
    )
    keyboard.row(
        InlineKeyboardButton('<', callback_data=f"dec_seconds:{minutes}:{seconds}"),
        InlineKeyboardButton(f"{seconds} {msg.get_message({'seconds': 'none'}, None, 0, 'keyboards')}",
                             callback_data=f"nothing"),
        InlineKeyboardButton('>', callback_data=f"inc_seconds:{minutes}:{seconds}"),
    )
    keyboard.row(
        InlineKeyboardButton(msg.get_message({'set_notification': 'none'}, None, 0, 'keyboards'),
                             callback_data=f"set_notification:{minutes}:{seconds}")
    )
    return keyboard

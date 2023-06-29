from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.utils.localization.i18n import MessageFormatter


def ikb_menu_bus_stops(user, bus_stops, not_delete: bool = True, text_callback_start: str = "stop"):
    inline_keyboard = []
    for i in range(0, len(bus_stops), 3):  # итерация с шагом 3
        row = []
        for bus_stop in bus_stops[i:i + 3]:  # добавление до трех остановок в одну строку
            row.append(InlineKeyboardButton(text=bus_stop.name,
                                            callback_data=f'{text_callback_start}_{bus_stop.id_stop}_{bus_stop.id}'))
        inline_keyboard.append(row)
    if not_delete:
        formatter = MessageFormatter(user.language, 'keyboards')
        # Добавление двух дополнительных кнопок в отдельных рядах
        inline_keyboard.append([InlineKeyboardButton(text=formatter.get_message(
                                           {'add_new_bus_stop': 'none'}, None, 0), callback_data='add_new_bus_stop')])
        inline_keyboard.append([InlineKeyboardButton(text=formatter.get_message(
                                           {'back_to_main_menu': 'none'}, None, 0), callback_data='back_to_main_menu')])

    ikb_bus_stops = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return ikb_bus_stops

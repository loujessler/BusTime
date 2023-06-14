from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.i18n import MessageFormatter


def ikb_menu_bus_stops(user, bus_stops, not_delete=True):
    inline_keyboard = []
    for i in range(0, len(bus_stops), 3):  # итерация с шагом 3
        row = []
        for bus_stop in bus_stops[i:i + 3]:  # добавление до трех остановок в одну строку
            row.append(InlineKeyboardButton(text=bus_stop.name,
                                            callback_data=f'stop_{bus_stop.id_stop}_{bus_stop.id}'))
        inline_keyboard.append(row)
    if not_delete:
        # Добавление двух дополнительных кнопок в отдельных рядах
        inline_keyboard.append([InlineKeyboardButton(text=MessageFormatter(user.language).get_message(
                                           {'add_new_bus_stop': 'none'}, None, 0, 'keyboards'), callback_data='add_new_bus_stop')])
        inline_keyboard.append([InlineKeyboardButton(text=MessageFormatter(user.language).get_message(
                                           {'back_to_main_menu': 'none'}, None, 0, 'keyboards'), callback_data='back')])

    ikb_bus_stops = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return ikb_bus_stops

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

text = {
    'ru': 'Добавить ещё',
    'en': 'Add new'
}


def ikb_menu_bus_stops(user, bus_stops):
    ikb_bus_stops = InlineKeyboardMarkup(row_width=3)
    for bus_stop in bus_stops:
        ikb_bus_stops.insert(InlineKeyboardButton(text=bus_stop.name,
                                                  callback_data=f'stop_{bus_stop.id_stop}_{bus_stop.id}'))
    ikb_bus_stops.insert(
        InlineKeyboardButton(text=text[user.language], callback_data='add_new_bus_stop'))
    return ikb_bus_stops

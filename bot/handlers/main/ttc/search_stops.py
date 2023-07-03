from loguru import logger

from aiogram import types

from bot.keyboards.inline.inline_kb_default import ikb_default
from bot.loader import dp, bot
from bot.utils.additional import number_to_emoji, capitalize_words

from bot.utils.data_utils.json_data import load_json_data
from bot.utils.data_utils.kd_tree import array_cord
from bot.utils.localization.i18n import MessageFormatter


@dp.message_handler(content_types=types.ContentType.LOCATION)
async def process_location(message: types.Message):
    user_id = message.from_user.id
    user = message.conf.get('user')
    bus_stops = await load_json_data('stops_data')

    # Пользовательская геолокация
    user_lat, user_lon = message.location.latitude, message.location.longitude

    # Ищем 5 ближайших остановок
    dist, ind = array_cord(bus_stops).query([[user_lat, user_lon]], k=5)

    msg_class = MessageFormatter(user.language)
    msg = msg_class.get_message({'found_stop_header': 'none'}) + '\n\n'
    keyboard = types.InlineKeyboardMarkup()
    buttons = []
    for i, (d, index) in enumerate(zip(dist[0], ind[0]), start=1):
        stop = bus_stops[index]

        name = stop['name'] if user.language == 'ka' else stop['name_translit']
        name = await capitalize_words(name)
        code = stop['code']
        # преобразуем евклидово расстояние в географическое расстояние
        distance = d * 111  # примерное преобразование для масштаба градусов в километры на широтах около 45 градусов
        msg += msg_class.get_message(
            {'found_stop': 'none'},
            {'i': number_to_emoji(i), 'name': name, 'code': code, 'distance': "%.2f" % distance}
        ) + '\n\n'
        button = types.InlineKeyboardButton(f'{i}', callback_data=f'found_{index}')
        buttons.append(button)
    msg += msg_class.get_message({'found_stop_footer': 'none'})
    keyboard.row(*buttons)
    keyboard.inline_keyboard += ikb_default(user.language).inline_keyboard
    await message.answer(text=msg, reply_markup=keyboard, parse_mode=types.ParseMode.MARKDOWN)
    # LOGS
    logger.log(25, f"The user {user_id} is looking for stops nearby.")


@dp.callback_query_handler(text_startswith='found_')
async def process_found_bus_stop(call: types.CallbackQuery):
    user_id = call.from_user.id
    user = call.conf.get('user')
    bus_stops = await load_json_data('stops_data')

    # Получаем данные из обратного вызова
    index = int(call.data.split('_')[1])
    stop = bus_stops[index]
    name = stop['name'] if user.language == 'ka' else stop['name_translit']
    name = await capitalize_words(name)
    code = stop['code']
    map_link = f'http://www.google.com/maps/place/{stop["lat"]},{stop["lon"]}'

    msg_locale = await bot.send_location(user_id, stop["lat"], stop["lon"])
    msg_locale_id = msg_locale.message_id
    await bot.send_message(
        user_id,
        MessageFormatter(user.language).get_message(
            {'found_stop_choose': 'none'},
            {'name': name, 'code': code, 'map_link': map_link}
        ),
        parse_mode=types.ParseMode.MARKDOWN,
        reply_markup=ikb_default(
            user.language,
            {'search_check_arrival': f'stop_{code}_wmap_{msg_locale_id}',
             'add_current_bus_stop': f'add_new_bus_stop_{name}_{code}_{msg_locale_id}',
             'back_to_main_menu': f'back_to_main_menu:message_id:{msg_locale_id}'}
        )
    )

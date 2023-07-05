from aiogram.dispatcher.filters import Regexp
from aiogram.types.web_app_info import WebAppInfo
from aiogram import types

from bot.loader import dp, bot

from bot.handlers.main.utils.route_pages_creator import PageBuilder
from bot.keyboards.inline.inline_kb_default import ikb_default
from bot.utils.localization.i18n import MessageFormatter
from data import config


@dp.message_handler(Regexp(r'\d+$'), is_bus=True)
async def command_start(message: types.Message):
    user = message.conf.get('user')
    route_number = message.text
    await bot.delete_message(message.chat.id, message.message_id)
    page_bldr = PageBuilder(route_number)

    forwards = await page_bldr.check_forwards()
    # Create Keyboard
    keyboard = types.InlineKeyboardMarkup()
    buttons = []
    for forward in forwards:
        html_name = await page_bldr.create_page(forward)
        route_url = f"http://127.0.0.1:8080/data/routes/{html_name}"
        if config.TEST_WEB_APP:
            route_url = f"https://bustime.ge/test/routes/{html_name}"
        else:
            route_url = f"https://bustime.ge/routes/{html_name}"
        web_app = WebAppInfo(url=route_url)
        button = types.InlineKeyboardButton(text=f'{forward}',
                                            web_app=web_app)
        buttons.append(button)
    keyboard.row(*buttons)
    keyboard.inline_keyboard += ikb_default(user.language).inline_keyboard
    # Create message
    msg = MessageFormatter(user.language).get_message(format_dict={'choose route': 'bold'},
                                                      format_args={'route_number': route_number}) + '\n\n'
    route_directions = await page_bldr.get_route_directions(forwards, user.language)
    for direction in route_directions:
        msg += direction + '\n\n'
    await bot.send_message(chat_id=message.chat.id,
                           text=msg,
                           reply_markup=keyboard)

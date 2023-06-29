from aiogram.types import CallbackQuery

from bot.loader import dp, bot

from bot.keyboards.inline import ikb_menu

from bot.handlers.main.bot_start import edit_ls
from bot.utils.localization.i18n import MessageFormatter


@dp.callback_query_handler(text_startswith='back_to_main_menu')
async def handler_back(call: CallbackQuery):
    # Получаем данные из обратного вызова
    callback_data = call.data
    splitted_data = callback_data.split(':')
    if len(splitted_data) > 1:
        if splitted_data[1] == 'message_id':
            await bot.delete_message(call.message.chat.id, splitted_data[2])

    user = call.conf.get('user')
    await edit_ls.edit_last_message(
        MessageFormatter(user.language).get_message({'welcome_message': 'bold',
                                                     'instructions_message': 'italic'},
                                                    None, 2),
        call,
        ikb_menu(user)
    )

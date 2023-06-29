from aiogram import types

from bot.loader import dp

from bot.keyboards.inline.inline_kb_default import ikb_default

from bot.utils.db_api import quick_commands as commands
from bot.utils.localization.i18n import MessageFormatter

from bot.handlers.main.bot_start import edit_ls


@dp.callback_query_handler(text='count_users')
async def count_users_func(call: types.CallbackQuery):
    user = call.conf.get('user')
    language = user.language
    count_users = await commands.count_users()
    await edit_ls.edit_last_message(
        MessageFormatter(language, 'admins').get_message(
            {'users': 'bold'},
            {'count_users': count_users},
            0),
        call,
        ikb_default(
            language,
            {'back_to_admin_menu': 'back_to_admin_menu',
             'back_to_main_menu': 'back_to_main_menu'}
        )
    )

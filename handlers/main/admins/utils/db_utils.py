from aiogram import types

from loader import dp

from keyboards.inline.inline_kb_default import ikb_default

from utils.db_api import quick_commands as commands
from utils.localization.i18n import MessageFormatter

from handlers.main.bot_start import edit_ls


@dp.callback_query_handler(text='count_users')
async def count_users_func(call: types.CallbackQuery):
    user = await commands.select_user(call.from_user.id)
    count_users = await commands.count_users()
    await edit_ls.edit_last_message(
        MessageFormatter(user.language).get_message(
            {'users': 'bold'},
            {'count_users': count_users},
            0,
            'admins'
        ),
        call,
        ikb_default(
            user,
            {'back_to_admin_menu': 'back_to_admin_menu',
             'back_to_main_menu': 'back_to_main_menu'}
        )
    )

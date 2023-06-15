from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp

from keyboards.inline.inline_kb_default import ikb_default

from utils.additional import return_msg_aio_type
from utils.db_api import quick_commands as commands
from utils.i18n import MessageFormatter

from handlers.main.bot_start import edit_ls


async def admin_menu(aio_type):
    user = await commands.select_user(aio_type.from_user.id)
    aio_type = return_msg_aio_type(aio_type)
    await aio_type.delete()
    await edit_ls.edit_last_message(
        MessageFormatter(user.language).get_message({'choose': 'bold'},
                                                    None, 0, 'admins'),
        aio_type,
        ikb_default(
            user,
            {'count_users': 'count_users',
             'back_to_main_menu': 'back_to_main_menu'}
        )
    )


@dp.message_handler(Command("admin", prefixes="/"), is_admin=True)
async def admin_handler(message: types.Message):
    await admin_menu(message)


@dp.callback_query_handler(text='back_to_admin_menu')
async def admin_handler_cmd(call: types.CallbackQuery):
    await admin_menu(call)


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

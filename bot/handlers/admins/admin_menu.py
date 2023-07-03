from aiogram import types
from aiogram.dispatcher.filters import Command

from bot.loader import dp, bot

from bot.keyboards.inline.inline_kb_default import ikb_default

from bot.utils.additional import return_msg_aio_type
from bot.utils.localization.i18n import MessageFormatter

from bot.utils.edit_last_message import EditLastMessage

edit_ls = EditLastMessage(bot)


async def admin_menu(aio_type):
    user = aio_type.conf.get('user')
    language = user.language
    aio_type = await return_msg_aio_type(aio_type)
    await edit_ls.edit_last_message(
        MessageFormatter(language, 'admins').get_message({'choose': 'bold'}, None, 0),
        aio_type,
        ikb_default(
            language,
            {'count_users': 'count_users',
             'refresh_json_data': 'refresh_json_data',
             'refresh_json_bus_routes': 'refresh_json_bus_routes',
             'back_to_main_menu': 'back_to_main_menu'
             }
        )
    )


@dp.message_handler(Command("admin", prefixes="/"), is_admin=True)
async def admin_handler(message: types.Message):
    await message.delete()
    await admin_menu(message)


@dp.callback_query_handler(text='back_to_admin_menu')
async def admin_handler_cmd(call: types.CallbackQuery):
    await admin_menu(call)

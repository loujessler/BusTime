from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message

from loader import dp

from filters import HaveInDb
from handlers.main.bot_start import edit_ls
from keyboards.inline.settings import ikb_menu_settings

from data.messages.settings_messages import Messages
from utils.db_api import quick_commands as commands


@dp.callback_query_handler(text='back_to_settings')
@dp.callback_query_handler(text='my settings')
async def handler_settings_menu(call: CallbackQuery):
    user = await commands.select_user(call.from_user.id)
    await edit_ls.edit_last_message(
        Messages(user).menu_msg(),
        call,
        ikb_menu_settings(user)
    )


@dp.message_handler(HaveInDb(True), Command('settings'))
async def settings_menu_command(message: Message):
    user = await commands.select_user(message.from_user.id)
    await message.delete()
    await edit_ls.edit_last_message(
        Messages(user).menu_msg(),
        message,
        ikb_menu_settings(user)
    )

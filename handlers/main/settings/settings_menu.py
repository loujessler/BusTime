from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message

from keyboards.inline.inline_kb_default import ikb_default
from loader import dp

from filters import HaveInDb
from handlers.main.bot_start import edit_ls

from data.languages import languages
from utils.db_api import quick_commands as commands
from utils.localization.i18n import MessageFormatter


@dp.callback_query_handler(text='back_to_settings')
@dp.callback_query_handler(text='my settings')
async def handler_settings_menu(call: CallbackQuery):
    user = await commands.select_user(call.from_user.id)
    await edit_ls.edit_last_message(
        MessageFormatter(user.language).get_message(
            {'setting_menu': 'bold',
             'setting_menu_lang': 'italic'},
            {'language': languages[user.language]}, 2
        ),
        call,
        ikb_default(user, {'change_language': 'change_language',
                           'settings_bus_stop': 'settings_bus_stop',
                           'back_to_main_menu': 'back_to_main_menu'})
    )


@dp.message_handler(HaveInDb(True), Command('settings'))
async def settings_menu_command(message: Message):
    await message.delete()
    await handler_settings_menu(message)

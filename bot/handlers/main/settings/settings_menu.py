from aiogram.types import CallbackQuery

from bot.loader import dp

from data.languages import languages
from bot.handlers.main.bot_start import edit_ls
from bot.keyboards.inline.inline_kb_default import ikb_default
from bot.utils.localization.i18n import MessageFormatter


@dp.callback_query_handler(text='my settings')
async def handler_settings_menu(call: CallbackQuery):
    user = call.conf.get('user')
    language = user.language
    await edit_ls.edit_last_message(
        MessageFormatter(language).get_message(
            {'setting_menu': 'bold',
             'setting_menu_lang': 'italic'},
            {'language': languages[user.language]}, 2
        ),
        call,
        ikb_default(language, {'change_language': 'change_language',
                               'settings_bus_stop': 'settings_bus_stop',
                               'back_to_main_menu': 'back_to_main_menu'})
    )

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.keyboards.inline.inline_kb_default import ikb_default
from bot.loader import dp

from data.languages import languages

from bot.keyboards.inline.language_inline_kb import ikb_languages

from bot.states.regist import Regist
from bot.utils.db_api import quick_commands as commands
from bot.utils.localization.i18n import MessageFormatter
from bot.utils.set_bot_commands import set_start_commands

from bot.handlers.main.bot_start import edit_ls


@dp.callback_query_handler(text='change_language')
async def change_language(call: types.CallbackQuery):
    user = call.conf.get('user')
    await edit_ls.edit_last_message(
        MessageFormatter(user.language).get_message(
            {'setting_change_language': 'bold'},
            None, 2
        ),
        call,
        ikb_languages
    )
    await Regist.change_language.set()


@dp.callback_query_handler(lambda c: c.data in [language for language in languages], state=Regist.change_language)
async def update_language(call: types.CallbackQuery, state: FSMContext):
    language = call.data
    await commands.update_language(call, language)
    await set_start_commands(call)
    await edit_ls.edit_last_message(
        MessageFormatter(language).get_message(
            {'setting_change_language_done': 'bold'}),
        call,
        ikb_default(language, {'back_to_settings': 'back_to_settings',
                               'back_to_main_menu': 'back_to_main_menu'})
    )
    await state.finish()

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp

from data.languages import languages

from keyboards.inline.language_inline_kb import ikb_languages
from keyboards.inline.settings import ikb_back_to_settings

from states.regist import Regist
from utils.db_api import quick_commands as commands
from utils.i18n import MessageFormatter
from utils.set_bot_commands import set_start_commands

from handlers.main.bot_start import edit_ls


@dp.callback_query_handler(text='change_language')
async def change_language(call: types.CallbackQuery):
    user = await commands.select_user(call.from_user.id)
    await edit_ls.edit_last_message(
        MessageFormatter(user).get_message(
            {'setting_change_language': 'bold'},
            None, 2
        ),
        call,
        ikb_languages
    )
    await Regist.change_language.set()


@dp.callback_query_handler(lambda c: c.data in [language for language in languages], state=Regist.change_language)
async def update_language(call: types.CallbackQuery, state: FSMContext):
    user = await commands.select_user(call.from_user.id)
    await commands.update_language(user.user_id, call.data)
    print(call.from_user.id, user.user_id)
    await set_start_commands(call.bot, call.from_user.id, user)
    user = await commands.select_user(call.from_user.id)
    await edit_ls.edit_last_message(
        MessageFormatter(user).get_message(
            {'setting_change_language_done': 'bold'}),
        call,
        ikb_back_to_settings(user)
    )
    await state.finish()

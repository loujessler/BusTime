from aiogram.types import CallbackQuery

from loader import dp

from handlers.main.bot_start import edit_ls

from keyboards.inline.inline_kb_default import ikb_default

from utils.db_api import quick_commands as commands
from utils.localization.i18n import MessageFormatter


@dp.callback_query_handler(text='settings_bus_stop')
async def settings_bus_stop(call: CallbackQuery):
    user = await commands.select_user(call.from_user.id)
    await edit_ls.edit_last_message(
        MessageFormatter(user.language).get_message({'settings_bus_stop': 'bold'}),
        call,
        ikb_default(user, {'add_new_bus_stop': 'add_new_bus_stop',
                           'change_name_bus_stop': 'change_name_bus_stop',
                           'change_code_bus_stop': 'change_code_bus_stop',
                           'delete_bus_stop': 'delete_bus_stop',
                           'back_to_settings': 'back_to_settings'})
    )

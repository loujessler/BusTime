from aiogram.types import CallbackQuery

from loader import dp

from keyboards.inline import ikb_menu

from handlers.main.bot_start import edit_ls
from utils.db_api import quick_commands as commands
from utils.i18n import MessageFormatter


@dp.callback_query_handler(text='back')
async def handler_back(call: CallbackQuery):
    user = await commands.select_user(call.from_user.id)
    await edit_ls.edit_last_message(
        MessageFormatter(user).get_message({'welcome_message': 'bold',
                                            'instructions_message': 'italic'},
                                           None, 2),
        call,
        ikb_menu(user)
    )


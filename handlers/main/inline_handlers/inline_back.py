from aiogram.types import CallbackQuery

from loader import dp

from keyboards.inline import ikb_menu
from data.messages.start_messages import Messages
from handlers.main.bot_start import edit_ls
from utils.db_api import quick_commands as commands


@dp.callback_query_handler(text='back')
async def handler_back(call: CallbackQuery):
    user = await commands.select_user(call.from_user.id)
    await edit_ls.edit_last_message(
        Messages(user).finish_registration(),
        call,
        ikb_menu(user)
    )


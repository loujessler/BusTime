from loader import dp
from aiogram.types import CallbackQuery

from data.messages.start_messages import Messages
from handlers.main.bot_start import edit_ls
from utils.db_api import quick_commands as commands


@dp.callback_query_handler(text='back')
async def send_message(call: CallbackQuery):
    user = await commands.select_user(call.from_user.id)
    # await call.message.edit_text(Messages(user).finish_registration(), parse_mode='HTML')
    await edit_ls.edit_last_message(
        Messages(user).finish_registration(),
        call
    )
    # await call.message.edit_reply_markup(ikb_menu(user))


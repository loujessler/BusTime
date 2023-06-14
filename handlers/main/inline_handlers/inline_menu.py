from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp
from filters import HaveInDb

from keyboards.inline import ikb_menu

from utils.db_api import quick_commands as commands
from handlers.main.bot_start import edit_ls
from utils.i18n import MessageFormatter


@dp.message_handler(Command('menu'), HaveInDb(True))
async def menu(message: types.Message):
    user = await commands.select_user(message.from_user.id)
    await message.delete()
    await edit_ls.edit_last_message(
        MessageFormatter(user.language).get_message({'welcome_message': 'bold',
                                                     'instructions_message': 'italic'},
                                                    None, 2),
        message,
        ikb_menu(user)
    )

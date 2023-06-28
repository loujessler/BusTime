from loguru import logger

from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp, bot

from utils.db_api import quick_commands as commands
from utils.localization.i18n import MessageFormatter

from keyboards.inline.inline_kb_default import ikb_default


@dp.message_handler(Command("help"), is_admin=True)
async def command_help(message: types.Message):
    await message.delete()
    user_id = message.from_user.id
    user = await commands.select_user(user_id)

    logger.log(25, f"The user {user_id} clicked on /help button.")

    await message.answer(
        MessageFormatter(user.language).get_message(
            format_dict={'help': 'bold',
                         'help_main': 'none',
                         'help_instruction': 'link'},
            line_breaks=2),
        parse_mode='HTML',
        reply_markup=ikb_default(user)
    )

from loguru import logger

from aiogram import types
from aiogram.dispatcher.filters import Command

from bot.loader import dp

from bot.utils.localization.i18n import MessageFormatter
from bot.keyboards.inline.inline_kb_default import ikb_default


@dp.message_handler(Command("help"), is_admin=True)
async def command_help(message: types.Message):
    await message.delete()
    user = message.conf.get('user')

    logger.log(25, f"The user {message.from_user.id} clicked on /help button.")

    await message.answer(
        MessageFormatter(user.language).get_message(
            format_dict={'help': 'bold',
                         'help_main': 'none',
                         'help_instruction': 'link'},
            line_breaks=2),
        parse_mode='HTML',
        reply_markup=ikb_default(user.language)
    )

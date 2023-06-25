from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp, bot

from utils.db_api import quick_commands as commands
from utils.localization.i18n import MessageFormatter

from keyboards.inline.inline_kb_default import ikb_default


@dp.message_handler(Command("help"), is_admin=True)
async def command_help(message: types.Message):
    await message.delete()
    user = await commands.select_user(message.from_user.id)
    instruction_link = 'https://telegra.ph/Instrukciya-06-25-10'
    await message.answer(
        MessageFormatter(user.language).get_message(
            {'help_main': 'none'},
            {'instruction_link': instruction_link}, 2),
        parse_mode=types.ParseMode.MARKDOWN,
        reply_markup=ikb_default(user)
    )

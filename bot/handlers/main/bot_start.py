from aiogram import types
from aiogram.dispatcher.filters import Command
from loguru import logger

from bot.loader import dp, bot

from bot.filters import IsPrivate

from bot.keyboards.inline import ikb_menu

from bot.utils.db_api import quick_commands as commands
from bot.utils.edit_last_message import EditLastMessage
from bot.utils.set_bot_commands import set_start_commands
from bot.utils.localization.i18n import MessageFormatter

edit_ls = EditLastMessage(bot)


async def main_menu(message: types.Message):
    user = message.conf.get('user')
    await edit_ls.edit_last_message(
        MessageFormatter(user.language).get_message({'welcome_message': 'bold',
                                                     'instructions_message': 'italic'},
                                                    None, 2),
        message,
        ikb_menu(user)
    )


@dp.message_handler(Command("start", prefixes="/"), IsPrivate())
async def command_start(message: types.Message):
    await main_menu(message)
    await set_start_commands(message)
    # LOGS
    logger.log(25, f"The user {message.from_user.id} clicked on /start button.")


@dp.message_handler(IsPrivate(), text='/ban')
async def get_ban(message: types.Message):
    await commands.update_status(message, 'ban')
    await message.answer('Ты забанен!')


@dp.message_handler(IsPrivate(), text='/unban')
async def get_ban(message: types.Message):
    await commands.update_status(message, 'active')
    await message.answer('Тебя разбанили!')

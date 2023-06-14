from aiogram import types
from aiogram.types import BotCommandScopeDefault, BotCommandScopeChat

from data.languages import languages
from loader import bot
from utils.i18n import MessageFormatter


async def set_default_commands():
    return await bot.set_my_commands(
        commands=[
            types.BotCommand('start', 'Start'),
        ],
        scope=BotCommandScopeDefault(),
    )


async def set_start_commands(aio_type):
    command_ids = {
        'menu': 'menu',
        'my_bus_stops': 'my_bus_stops',
        'settings': 'settings',
        'help': 'help'
    }

    if aio_type.from_user.language_code not in languages:
        language = 'en'
    else:
        language = aio_type.from_user.language_code

    formatter = MessageFormatter(language)

    commands = []
    for command, msg_id in command_ids.items():
        description = formatter.get_message({msg_id: 'none'}, domain='menu_commands')
        commands.append(types.BotCommand(command, description))

    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeChat(aio_type.message.chat.id),
        language_code=language
    )

from aiogram import types
from aiogram.types import BotCommandScopeDefault, BotCommandScopeChat

from utils.i18n import MessageFormatter


async def set_default_commands(bot):
    return await bot.set_my_commands(
        commands=[
            types.BotCommand('start', 'Start'),
        ],
        scope=BotCommandScopeDefault(),
    )


async def set_start_commands(bot, chat_id, user):
    command_ids = {
        'menu': 'menu',
        'my_bus_stops': 'my_bus_stops',
        'settings': 'settings',
        'help': 'help'
    }

    formatter = MessageFormatter(user)

    commands = []
    for command, msg_id in command_ids.items():
        description = formatter.get_message({msg_id: 'none'}, domain='menu_commands')
        commands.append(types.BotCommand(command, description))

    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeChat(chat_id),
        language_code=user.language
    )



# async def set_start_commands(bot, chat_id, language):
#     text_commands = {
#         'ru': [
#             types.BotCommand('menu', 'Главное меню'),
#             types.BotCommand('my_bus_stops', '🚏 Мои остановки'),
#             types.BotCommand('settings', '⚙️ Настройки'),
#             types.BotCommand('help', '💬 Помощь'),
#         ],
#         'en': [
#             types.BotCommand('menu', 'Main menu'),
#             types.BotCommand('my_bus_stops', '🚏 My bus stops'),
#             types.BotCommand('settings', '⚙️ Settings'),
#             types.BotCommand('help', '💬 Help'),
#         ],
#         'ka': [
#             types.BotCommand('menu', 'მთავარი მენიუ'),
#             types.BotCommand('my_bus_stops', '🚏 ჩემი გაჩერებული გაჩერება'),
#             types.BotCommand('settings', '⚙️ პარამეტრები'),
#             types.BotCommand('help', '💬 დახმარება'),
#         ],
#     }
#     for language_code, commands in text_commands.items():
#         await bot.set_my_commands(
#             commands=commands,
#             scope=BotCommandScopeChat(chat_id),
#             language_code=language_code
#         )

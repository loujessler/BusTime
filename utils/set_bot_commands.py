from aiogram import types
from aiogram.types import BotCommandScopeDefault, BotCommandScopeChat


async def set_default_commands(bot):
    return await bot.set_my_commands(
        commands=[
            types.BotCommand('start', 'Start'),
        ],
        scope=BotCommandScopeDefault(),
    )


async def set_start_commands(bot, chat_id, language):
    text_commands = {
        'ru': [
            types.BotCommand('menu', 'Главное меню'),
            types.BotCommand('my_bus_stops', '🚏 Мои остановки'),
            types.BotCommand('settings', '⚙️ Настройки'),
            types.BotCommand('help', '💬 Помощь'),
        ],
        'en': [
            types.BotCommand('menu', 'Main menu'),
            types.BotCommand('my_bus_stops', '🚏 My bus stops'),
            types.BotCommand('settings', '⚙️ Settings'),
            types.BotCommand('help', '💬 Help'),
        ],
        'ka': [
            types.BotCommand('menu', 'მთავარი მენიუ'),
            types.BotCommand('my_bus_stops', '🚏 ჩემი გაჩერებული გაჩერება'),
            types.BotCommand('settings', '⚙️ პარამეტრები'),
            types.BotCommand('help', '💬 დახმარება'),
        ],
    }
    for language_code, commands in text_commands.items():
        print(language_code, commands)
        await bot.set_my_commands(
            commands=commands,
            scope=BotCommandScopeChat(chat_id),
            language_code=language_code
        )

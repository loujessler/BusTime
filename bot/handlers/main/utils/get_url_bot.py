from bot.loader import bot


async def get_bot_link():
    bot_info = await bot.get_me()
    bot_link = f"https://t.me/{bot_info['username']}"
    return bot_link

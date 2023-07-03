from aiogram import executor
from bot.handlers import dp
from bot.loader import shutdown
from bot.bot import on_startup

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=shutdown)

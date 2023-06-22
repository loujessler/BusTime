import os


async def on_startup(dp):

    from loader import db
    from utils.db_api.db_gino import on_startup
    await on_startup(dp)

    # Получаем список таблиц в базе данных
    table_name = 'users'
    query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = '{table_name}')"
    result = await db.bind.scalar(query)
    table_exists = result

    if not table_exists:  # Проверяем, есть ли таблицы в базе данных
        # Создание и удаление базы данных
        await db.gino.drop_all()
        await db.gino.create_all()

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)

    from utils.set_bot_commands import set_default_commands
    await set_default_commands()

    # Запуск aiohttp сервера
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '127.0.0.1', 8080)
    await site.start()


if __name__ == '__main__':
    import asyncio
    from aiogram import executor
    from handlers import dp
    from loader import shutdown, bot, app

    from aiohttp import web

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=shutdown)



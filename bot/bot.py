from aiogram import exceptions
from loguru import logger


async def on_startup(dp):
    try:
        from .loader import db
        from .utils.db_api.db_gino import on_startup
        await on_startup(dp)

        # Получаем список таблиц в базе данных
        table_name = 'users'
        query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables " \
                f"WHERE table_schema = 'public' AND table_name = '{table_name}')"
        result = await db.bind.scalar(query)
        table_exists = result

        if not table_exists:  # Проверяем, есть ли таблицы в базе данных
            # Создание и удаление базы данных
            await db.gino.drop_all()
            await db.gino.create_all()

        from .utils.notify_admins import on_startup_notify
        await on_startup_notify(dp)

        from .utils.set_bot_commands import set_default_commands
        await set_default_commands()
    except exceptions.NetworkError as e:
        logger.warning(f"A NetworkError occurred: {e}")

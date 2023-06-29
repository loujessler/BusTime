from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiohttp.web_app import Application

from data import config
from .log_inter import InterceptHandler, LoguruLogger

from .middleware.anti_spam import AntiSpamMiddleware
from .middleware.get_user_db import GetUserMiddleware

from .utils.localization.compilation_languages import compile_translations
from .utils.db_api.db_gino import db

import logging
from bot import filters

# logging.basicConfig(format=u'[%(asctime)s]  #%(levelname)-8s [%(filename)s LINE:%(lineno)d] %(message)s',
#                     filename="py_log.log",
#                     level=config.DEBUG)

# Использование logs:
logger_obj = LoguruLogger()
logger_obj.setup_loguru()
logging.basicConfig(handlers=[InterceptHandler()], level=0)

bot = Bot(token=config.API_TOKEN, parse_mode=types.ParseMode.HTML, timeout=60)

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)

dp.middleware.setup(GetUserMiddleware())
dp.middleware.setup(AntiSpamMiddleware())

# set filters
filters.setup(dp)

compile_translations(config.LOCALES_DIR)

# Web
app = Application()
from .web.routers import home

# Добавление обработчиков в роутер приложения
# app.router.add_get('/data/routes/{name}', handle)
app.router.add_static('/data/routes/', path='data/routes/', name='routes')
app.router.add_get('/', home)


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


__all__ = ['bot', 'db', 'storage', 'dp']

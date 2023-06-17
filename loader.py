from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config

from utils.localization.compilation_languages import compile_translations
from utils.db_api.db_gino import db

import logging
import filters

# Level       Numeric value
# CRITICAL         50
# ERROR            40
# WARNING          30
# INFO             20
# DEBUG            10
# NOTSET            0

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    filename="py_log.log",
                    level=int(config.DEBUG))

bot = Bot(token=config.API_TOKEN, parse_mode=types.ParseMode.HTML)

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)

# set filters
filters.setup(dp)

compile_translations(config.LOCALES_DIR)


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


__all__ = ['bot', 'db', 'storage', 'dp']

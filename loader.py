from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config

from utils.compilation_languages import compile_translations
from utils.db_api.db_gino import db

import logging


debug = logging.DEBUG if config.DEBUG else logging.INFO
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    # filename="py_log.log",
                    level=debug)

bot = Bot(token=config.API_TOKEN, parse_mode=types.ParseMode.HTML)

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)

compile_translations(config.LOCALES_DIR)


# # Here we create a gettext translation object
# t = gettext.translation(I18N_DOMAIN, localedir=LOCALES_DIR, languages=['en'])
# _ = t.gettext  # We get the function that will return translated strings
# _ = I18n().get_translator()


# def set_language(language):
#     return gettext.translation(I18N_DOMAIN, localedir=LOCALES_DIR, languages=[language])


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


__all__ = ['bot', 'db', 'storage', 'dp']

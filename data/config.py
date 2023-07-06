import os
import json

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

API_TOKEN = str(os.environ.get("API_TOKEN"))

# This is machine is server
SERVER_MODE = int(os.getenv('SERVER_MODE'))

# Получение строки из переменной окружения
str_admins = os.getenv('ADMINS')
# Конвертация JSON строки обратно в список
ADMINS = json.loads(str_admins)
# База данных
ip = str(os.getenv('ip'))
POSTGRES_USER = str(os.getenv('POSTGRES_USER'))
POSTGRES_PASSWORD = str(os.getenv('POSTGRES_PASSWORD'))
DATABASE = str(os.getenv('DATABASE'))

POSTGRES_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{ip}/{DATABASE}'
# Дополнительные параметры
# Настройка i18n
I18N_DOMAIN = 'bustime'
LOCALES_DIR = str(os.getenv('LOCALES_DIR'))

DEBUG = int(os.getenv('DEBUG'))
REFRESH_HTML_FILES = int(os.getenv('REFRESH_HTML_FILES'))

TEST_WEB_APP = int(os.getenv('TEST_WEB_APP'))

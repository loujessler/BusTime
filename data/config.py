import os

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

API_TOKEN = str(os.environ.get("API_TOKEN"))

ADMINS = [
    6405640
]

ip = str(os.getenv('ip'))
POSTGRES_USER = str(os.getenv('POSTGRES_USER'))
POSTGRES_PASSWORD = str(os.getenv('POSTGRES_PASSWORD'))
DATABASE = str(os.getenv('DATABASE'))
DEBUG = str(os.getenv('DEBUG'))
# Настройка i18n
I18N_DOMAIN = 'bustime'
LOCALES_DIR = str(os.getenv('LOCALES_DIR'))

POSTGRES_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{ip}/{DATABASE}'

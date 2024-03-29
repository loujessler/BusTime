from aiogram import types

from bot.loader import dp

from bot.handlers.main.ttc.ttc_requests.get_ttc_api import GetTTC


# По нажатию на остановку показываем расписание остановки
@dp.message_handler(content_types=['web_app_data'])
async def get_webapp_data(message: types.Message):
    await GetTTC().arrival(message, message.web_app_data.data)

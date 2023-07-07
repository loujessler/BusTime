from aiogram import types
from aiogram.dispatcher.filters import Regexp

from bot.loader import dp

from bot.keyboards.inline.inline_kb_default import ikb_default
from bot.handlers.main.bot_start import edit_ls
from bot.utils.localization.i18n import MessageFormatter


# # Хэндлер для обработки несуществующих автобусов или остановок
@dp.message_handler(Regexp(r'^\d+$'), is_bus_stop=False, is_bus=False)
async def handle_bus_stop_message(message: types.Message):
    user = message.conf.get('user')
    await message.delete()
    message_data = [MessageFormatter(user.language).get_message({'arrival_bus_stop_or_bus_not_exists': 'bold'}),
                    ikb_default(user.language, {
                        'back_to_main_menu': 'back_to_main_menu',
                    })]
    await edit_ls.edit_last_message(message_data[0], message, message_data[1])

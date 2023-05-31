from aiogram import types
from aiogram.dispatcher.filters import Command

# from data.messages.messages import Messages
from data.messages.start_messages import Messages
from filters import HaveInDb
from keyboards.inline import ikb_menu
from loader import dp
from utils.db_api import quick_commands as commands
from handlers.main.bot_start import edit_ls


@dp.message_handler(Command('menu'), HaveInDb(True))
async def menu(message: types.Message):
    user = await commands.select_user(message.from_user.id)
    await message.delete()
    # await message.answer(Messages(user).finish_registration(), reply_markup=ikb_menu(user))
    await message.answer(Messages(user).finish_registration())
    # await edit_ls.edit_last_message(
    #     Messages(user).finish_registration(),
    #     message
    # )

# @dp.callback_query_handler(text='back')
# async def send_message(call: CallbackQuery):
#     user = await commands.select_user(call.from_user.id)
#     # await call.message.edit_text(Messages(user).finish_registration(), parse_mode='HTML')
#     await edit_ls.edit_last_message(
#         Messages(user).finish_registration(),
#         call
#     )
#     # await call.message.edit_reply_markup(ikb_menu(user))
from data.languages import languages
from filters import IsPrivate, HaveInDb

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import ikb_menu
from keyboards.inline.language_inline_kb import ikb_languages
from loader import dp, bot

from states.regist import Regist
from utils.db_api import quick_commands as commands
from utils.edit_last_message import EditLastMessage
from utils.set_bot_commands import set_start_commands
from data.messages.start_messages import Messages

edit_ls = EditLastMessage(bot)


@dp.message_handler(IsPrivate(), text='/start')
async def command_start(message: types.Message):
    user = await commands.select_user(message.from_user.id)
    try:
        if user.status == 'active':
            await message.answer(
                Messages(user).finish_registration(),
                parse_mode='HTML'
            )
            await message.edit_reply_markup(reply_markup=ikb_menu(user))
        elif user.status == 'baned':
            await message.answer('Ты забанен!')
    except Exception:
        await message.answer(
            Messages.language_mes(message),
            parse_mode='HTML',
            reply_markup=ikb_languages
        )
        await Regist.language.set()


@dp.callback_query_handler(HaveInDb(False), lambda c: c.data in [language for language in languages],
                           state=Regist.language)
async def first_message(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(language=call.data)
    data = await state.get_data()
    await commands.add_user(user_id=call.from_user.id,
                            first_name=call.from_user.first_name,
                            last_name=call.from_user.last_name,
                            username=call.from_user.username,
                            status='active',
                            language=data.get('language'),
                            )
    user = await commands.select_user(call.from_user.id)
    await set_start_commands(call.bot, call.from_user.id, data.get('language'))
    await edit_ls.edit_last_message(
        Messages(user).finish_registration(),
        call
    )
    await state.finish()

# @dp.callback_query_handler(HaveInDb(False), lambda c: c.data in [language for language in languages],
#                            state=Regist.language)
# async def create_password(call: types.CallbackQuery, state: FSMContext):
#     await state.update_data(language=call.data)
#     await edit_ls.edit_last_message(
#         Messages.first_pas_mes(call.data, call),
#         call
#     )
#     await Regist.password.set()

#
# @dp.message_handler(IsPrivate(), state=Regist.password)
# async def reply_password(message: types.Message, state: FSMContext):
#     await state.update_data(password=message.text)
#     data = await state.get_data()
#     await bot.delete_message(message.from_user.id, message.message_id)
#     await edit_ls.edit_last_message(
#         Messages.reply_password[data.get('language')],
#         message
#     )
#     await Regist.next()


# @dp.message_handler(IsPrivate(), state=Regist.language)
# async def create_user_wallet(message: types.Message, state: FSMContext):
#     await state.update_data(reply_password=message.text)
#     data = await state.get_data()
#     await bot.delete_message(message.from_user.id, message.message_id)
#
#     await state.update_data(reply_password=message.text)
#
#     await commands.add_user(user_id=message.from_user.id,
#                             first_name=message.from_user.first_name,
#                             last_name=message.from_user.last_name,
#                             username=message.from_user.username,
#                             status='active',
#                             language=data.get('language'),
#                             )
#     user = await commands.select_user(message.from_user.id)
#     await set_start_commands(message.bot, message.from_user.id, data.get('language'))
#     await edit_ls.edit_last_message(
#         Messages.finish_registration(user),
#         message
#     )
#     await state.finish()


@dp.message_handler(IsPrivate(), text='/ban')
async def get_ban(message: types.Message):
    user = await commands.select_user(message.from_user.id)
    await commands.update_status(user, 'ban')
    await message.answer('Ты забанен!')


@dp.message_handler(IsPrivate(), text='/unban')
async def get_ban(message: types.Message):
    user = await commands.select_user(message.from_user.id)
    await commands.update_status(user, 'active')
    await message.answer('Тебя разбанили!')

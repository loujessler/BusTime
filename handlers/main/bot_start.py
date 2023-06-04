from aiogram import types
import aiogram.utils.markdown as fmt
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from data.languages import languages

from filters import IsPrivate, HaveInDb

from keyboards.inline import ikb_menu
from keyboards.inline.language_inline_kb import ikb_languages

from loader import dp, bot

from states.regist import Regist

from utils.db_api import quick_commands as commands
from utils.edit_last_message import EditLastMessage
from utils.set_bot_commands import set_start_commands
from utils.i18n import MessageFormatter

edit_ls = EditLastMessage(bot)


@dp.message_handler(Command("start", prefixes="/"), IsPrivate())
async def command_start(message: types.Message):
    user_id = message.from_user.id
    user = await commands.select_user(user_id)
    language_mes = fmt.text(
        f'✌️ Hi, {message.from_user.first_name}.\n',
        fmt.hbold('🏳️ Choose your language: ')
    )
    if user is None:
        await message.answer(
            language_mes,
            parse_mode='HTML',
            reply_markup=ikb_languages
        )
        await Regist.language.set()
        return

    if user.status == 'active':
        text = MessageFormatter(user).get_message({'welcome_message': 'bold',
                                                   'instructions_message': 'italic'},
                                                  None, 2)
        markup = ikb_menu(user)
    elif user.status == 'baned':
        text = 'Ты забанен!'
        markup = None
    else:
        return

    await message.answer(
        text,
        parse_mode='HTML',
        reply_markup=markup
    )


@dp.callback_query_handler(HaveInDb(False), lambda c: c.data in [language for language in languages],
                           state=Regist.language)
async def first_message(call: types.CallbackQuery, state: FSMContext):
    language = call.data

    # # Set the chosen language
    # global _
    # _ = set_language(language).gettext

    await state.update_data(language=language)
    user_id = call.from_user.id
    first_name = call.from_user.first_name
    last_name = call.from_user.last_name
    username = call.from_user.username

    try:
        await commands.add_user(user_id=user_id,
                                first_name=first_name,
                                last_name=last_name,
                                username=username,
                                status='active',
                                language=language)
    except Exception as e:
        # Here you can add logging or additional error handling
        raise e

    user = await commands.select_user(user_id)
    if user is not None:
        await set_start_commands(call.bot, user_id, language)
        await edit_ls.edit_last_message(
            MessageFormatter(user).get_message({'welcome_message': 'bold',
                                                'instructions_message': 'italic'},
                                               None, 2),
            call, ikb_menu(user)
        )

    await state.finish()


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

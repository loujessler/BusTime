from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp, bot

from filters import IsPrivate
from data.languages import languages

from keyboards.inline import ikb_menu

from utils.db_api import quick_commands as commands
from utils.edit_last_message import EditLastMessage
from utils.set_bot_commands import set_start_commands
from utils.localization.i18n import MessageFormatter

edit_ls = EditLastMessage(bot)


async def create_user(aio_type: types.Message):
    user_data = {'user_id': aio_type.from_user.id,
                 'first_name': aio_type.from_user.first_name,
                 'last_name': aio_type.from_user.last_name,
                 'username': aio_type.from_user.username}

    if aio_type.from_user.language_code not in languages:
        user_data['language'] = 'en'
    elif aio_type.from_user.language_code == 'be':
        user_data['language'] = 'ru'
    else:
        user_data['language'] = aio_type.from_user.language_code

    try:
        await commands.add_user(user_id=user_data['user_id'],
                                first_name=user_data['first_name'],
                                last_name=user_data['last_name'],
                                username=user_data['username'],
                                status='active',
                                language=user_data['language'])
    except Exception as e:
        # Here you can add logging or additional error handling
        raise e


@dp.message_handler(Command("start", prefixes="/"), IsPrivate())
async def command_start(message: types.Message):
    user = await commands.select_user(message.from_user.id)
    if user is None:
        await create_user(message)
        user = await commands.select_user(message.from_user.id)

    if user.status == 'active':
        text = MessageFormatter(user.language).get_message(
            {'welcome_message': 'bold',
             'instructions_message': 'italic'},
            None, 2)
        markup = ikb_menu(user)
    elif user.status == 'baned':
        text = 'Ты забанен!'
        markup = None
    else:
        return

    await set_start_commands(message)
    await message.answer(
        text,
        parse_mode='HTML',
        reply_markup=markup
    )


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

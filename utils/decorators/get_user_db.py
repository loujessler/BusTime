from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from utils.db_api import quick_commands as commands


def ctm_callback_query_handler(*dec_args, **dec_kwargs):
    def decorator(func):
        @dp.callback_query_handler(*dec_args, **dec_kwargs)
        async def wrapper(call: types.CallbackQuery):
            user = await commands.select_user(call.from_user.id)
            return await func(call, user, *dec_args, **dec_kwargs)
        return wrapper
    return decorator


def ctm_message_handler(*dec_args, **dec_kwargs):
    def decorator(func):
        @dp.message_handler(*dec_args, **dec_kwargs)
        async def wrapper(message: types.Message, *args, **kwargs):
            user = await commands.select_user(message.from_user.id)
            return await func(message, user, *args, **kwargs)
        return wrapper
    return decorator


def get_user_db(func, **kwargs):
    async def decorator(event: types.CallbackQuery or types.Message, state: FSMContext):
        user = await commands.select_user(event.from_user.id)
        return await func(event, user, state, **kwargs)
    return decorator

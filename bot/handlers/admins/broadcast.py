from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.utils.exceptions import BotBlocked, ChatNotFound

from bot.loader import dp, bot
from bot.states.broadcast_state import BroadcastStates
from bot.handlers.main.utils.cancel import cancel_func
from bot.utils.db_api import quick_commands as commands
from bot.utils.edit_last_message import EditLastMessage

edit_ls = EditLastMessage(bot)


@dp.message_handler(Command("broadcast", prefixes="/"), is_admin=True)
async def enter_broadcast_text(message: types.Message):
    sent_message = await message.answer("Please, send the content for broadcast. (/cancel)")
    BroadcastStates.msg.message_id = sent_message.message_id  # Сохраняем message_id
    # Set state
    await BroadcastStates.msg.set()


# Отмена при определенных состояниях
@dp.message_handler(Command('cancel'), is_admin=True, state=BroadcastStates.msg)
async def cancel_state_bus_stops(message: types.Message, state: FSMContext):
    state_mapping = {
        'BroadcastStates:msg': BroadcastStates.msg,
    }
    format_dict = {'bus_stops_finish_cancel': 'none'}
    user = message.conf.get('user')
    await cancel_func(message, user.language, state, state_mapping, format_dict)


@dp.message_handler(is_admin=True, state=BroadcastStates.msg, content_types=types.ContentType.ANY)
async def broadcast_text(message: types.Message, state: FSMContext):
    # Fetch users from database
    users = await commands.select_all_users()

    for user in users:
        try:
            await message.send_copy(chat_id=user.user_id,
                                    allow_sending_without_reply=True)
            if user.status == 'unsubscribed':
                await commands.update_status(message, "active", user.user_id)
        except (BotBlocked, ChatNotFound):
            await commands.update_status(message, "unsubscribed", user.user_id)

    # Reset state
    await state.finish()

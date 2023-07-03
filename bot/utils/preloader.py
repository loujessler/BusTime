from bot.loader import bot

from bot.utils.edit_last_message import EditLastMessage
edit_ls = EditLastMessage(bot)


# loading_messages = ['🕐', '🕑', '🕒', '🕓', '🕔', '🕕', '🕖', '🕗', '🕘', '🕙', '🕚', '🕛']
# loading_messages = ['🕛', '🕧', '🕐', '🕜', '🕑', '🕝', '🕒', '🕞', '🕓', '🕟', '🕔', '🕠', '🕕', '🕡',
#                     '🕖', '🕢', '🕗', '🕣', '🕘', '🕤', '🕙', '🕥', '🕚', '🕦']


async def show_loading_message(aio_type, event):
    loading_messages = '⏳'
    message = await edit_ls.edit_last_message(new_msg_text=loading_messages, aio_type=aio_type, return_msg_info=True)
    await event.wait()
    await bot.delete_message(chat_id=aio_type.chat.id, message_id=message.message_id)

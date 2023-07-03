from loguru import logger

from aiogram import exceptions
from bot.utils.additional import return_msg_aio_type


class EditLastMessage:
    def __init__(self, bot):
        self.bot = bot

    async def edit_last_message(self, new_msg_text: str, aio_type, new_keyboard=None, parse_mode='HTML',
                                return_msg_info=False):
        # Получаем идентификатор чата в зависимости от типа входящего объекта
        message = await return_msg_aio_type(aio_type)

        if message is not None:
            chat_id = message.chat.id
            message_id = message.message_id

            try:
                # Попытка редактировать сообщение
                sent_message = await self.bot.edit_message_text(
                    chat_id=chat_id, message_id=message_id,
                    text=new_msg_text, reply_markup=new_keyboard,
                    parse_mode=parse_mode)
            except (exceptions.MessageCantBeEdited, exceptions.MessageToEditNotFound):
                # Если сообщение невозможно отредактировать, отправляем новое
                sent_message = await self.bot.send_message(
                    chat_id=chat_id, text=new_msg_text,
                    reply_markup=new_keyboard,
                    parse_mode=parse_mode)
            except exceptions.MessageNotModified:
                sent_message = None

            if return_msg_info:
                return sent_message
        else:
            logger.warning("Invalid aio_type. Expected types.Message or types.CallbackQuery.")
            return None

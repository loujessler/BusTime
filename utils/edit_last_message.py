from aiogram import exceptions
from utils.additional import return_msg_aio_type


class EditLastMessage:
    def __init__(self, bot):
        self.bot = bot

    async def edit_last_message(self, new_message_text, aio_type, new_keyboard=None, parse_mode='HTML',
                                return_message_info=False):
        # Получаем идентификатор чата в зависимости от типа входящего объекта
        message = await return_msg_aio_type(aio_type)

        if message is not None:
            chat_id = message.chat.id
            message_id = message.message_id

            try:
                # Попытка редактировать сообщение
                sent_message = await self.bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                                                text=new_message_text, parse_mode=parse_mode)

                # Если предоставлена новая клавиатура, редактируем клавиатуру сообщения
                if new_keyboard is not None:
                    await self.bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                                             reply_markup=new_keyboard)
                if return_message_info:
                    return sent_message
            except (exceptions.MessageCantBeEdited, exceptions.MessageToEditNotFound):
                # Если сообщение невозможно отредактировать, отправляем новое
                sent_message = await self.bot.send_message(chat_id=chat_id, text=new_message_text,
                                                           reply_markup=new_keyboard,
                                                           parse_mode=parse_mode)

                if return_message_info:
                    return sent_message
        else:
            print("Invalid aio_type. Expected types.Message or types.CallbackQuery.")
            return None

# Version 3
# class EditLastMessage:
#     def __init__(self, bot):
#         self.bot = bot
#
#     async def edit_last_message(self, new_message_text, aio_type, new_keyboard=None, parse_mode='HTML'):
#         # Получаем идентификатор чата в зависимости от типа входящего объекта
#         message = return_msg_aio_type(aio_type)
#
#         if message is not None:
#             chat_id = message.chat.id
#             message_id = message.message_id
#
#             try:
#                 # Попытка редактировать сообщение
#                 await self.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=new_message_text,
#                                                  parse_mode=parse_mode)
#
#                 # Если предоставлена новая клавиатура, редактируем клавиатуру сообщения
#                 if new_keyboard is not None:
#                     await self.bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
#                                                              reply_markup=new_keyboard)
#             except (exceptions.MessageCantBeEdited, exceptions.MessageToEditNotFound):
#                 # Если сообщение невозможно отредактировать, отправляем новое
#                 await self.bot.send_message(chat_id=chat_id, text=new_message_text, reply_markup=new_keyboard,
#                                             parse_mode=parse_mode)
#         else:
#             print("Invalid aio_type. Expected types.Message or types.CallbackQuery.")

# Version 2
# async def edit_last_message(self, edit_message, aio_type, ikb=None, parse_mode='HTML'):
#     # message = return_msg_aio_type(aio_type)
#     i = 0
#     while True:
#         if i > 10:
#             await self.bot.send_message(aio_type.from_user.id,
#                                         edit_message,
#                                         reply_markup=ikb,
#                                         parse_mode=parse_mode)
#             break
#         else:
#             try:
#                 message_id = return_msg_aio_type(aio_type).message_id - i
#                 # if hasattr(aio_type, 'message_id'):
#                 #     message_id = aio_type.message_id - i
#                 # else:
#                 #     message_id = aio_type.message.message_id - i
#                 await self.bot.edit_message_text(edit_message,
#                                                  aio_type.from_user.id,
#                                                  message_id,
#                                                  parse_mode=parse_mode)
#                 break
#             except Exception as e:
#                 print(f"Exception while trying to edit message: {e}")
#                 i += 1
#
#     if ikb is not None:
#         try:
#             if hasattr(aio_type, 'message_id'):
#                 message_id = aio_type.message_id - i
#             else:
#                 message_id = aio_type.message.message_id - i
#             await self.bot.edit_message_reply_markup(aio_type.from_user.id,
#                                                      message_id,
#                                                      reply_markup=ikb)
#         except Exception as e:
#             print(f"Exception while trying to edit reply markup: {e}")

# Version 1
# async def edit_last_message(self, edit_message, aio_type, ikb=None, parse_mode='HTML'):
#     i = 0
#     while True:
#         if i > 10:
#             await self.bot.send_message(aio_type.from_user.id,
#                                         edit_message,
#                                         reply_markup=ikb,
#                                         parse_mode=parse_mode)
#             break
#         else:
#             try:
#                 if hasattr(aio_type, 'message_id'):
#                     message_id = aio_type.message_id - i
#                 else:
#                     message_id = aio_type.message.message_id - i
#                 await self.bot.edit_message_text(edit_message,
#                                                  aio_type.from_user.id,
#                                                  message_id,
#                                                  parse_mode=parse_mode)
#                 break
#             except Exception:
#                 i += 1
#                 pass
#     if ikb is not None:
#         try:
#             if hasattr(aio_type, 'message_id'):
#                 message_id = aio_type.message_id - i
#             else:
#                 message_id = aio_type.message.message_id - i
#             await self.bot.edit_message_reply_markup(aio_type.from_user.id,
#                                                      message_id,
#                                                      reply_markup=ikb)
#         except Exception:
#             pass

# async def edit_last_message(self, edit_message, aio_type, ikb=None, parse_mode='HTML'):
#     i = 0
#     while True:
#         if i > 10:
#             await self.bot.send_message(aio_type.from_user.id,
#                                         edit_message,
#                                         reply_markup=ikb,
#                                         parse_mode=str(parse_mode)
#                                         )
#             break
#         else:
#             try:
#                 try:
#                     message_id = (aio_type.message_id - i)
#                 except:
#                     message_id = (aio_type.message.message_id - i)
#                 await self.bot.edit_message_text(edit_message,
#                                                  aio_type.from_user.id,
#                                                  message_id,
#                                                  parse_mode=str(parse_mode))
#                 break
#             except Exception:
#                 i += 1
#                 pass
#     if ikb is not None:
#         try:
#             message_id = (aio_type.message_id - i)
#         except:
#             message_id = (aio_type.message.message_id - i)
#         await self.bot.edit_message_reply_markup(aio_type.from_user.id,
#                                                  message_id,
#                                                  reply_markup=ikb)

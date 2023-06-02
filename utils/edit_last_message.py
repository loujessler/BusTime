from utils.additional import return_msg_aio_type


class EditLastMessage:
    def __init__(self, bot):
        self.bot = bot

    async def edit_last_message(self, edit_message, aio_type, ikb=None, parse_mode='HTML'):
        # message = return_msg_aio_type(aio_type)
        i = 0
        while True:
            if i > 10:
                await self.bot.send_message(aio_type.from_user.id,
                                            edit_message,
                                            reply_markup=ikb,
                                            parse_mode=parse_mode)
                break
            else:
                try:
                    message_id = return_msg_aio_type(aio_type).message_id - i
                    # if hasattr(aio_type, 'message_id'):
                    #     message_id = aio_type.message_id - i
                    # else:
                    #     message_id = aio_type.message.message_id - i
                    await self.bot.edit_message_text(edit_message,
                                                     aio_type.from_user.id,
                                                     message_id,
                                                     parse_mode=parse_mode)
                    break
                except Exception as e:
                    print(f"Exception while trying to edit message: {e}")
                    i += 1

        if ikb is not None:
            try:
                if hasattr(aio_type, 'message_id'):
                    message_id = aio_type.message_id - i
                else:
                    message_id = aio_type.message.message_id - i
                await self.bot.edit_message_reply_markup(aio_type.from_user.id,
                                                         message_id,
                                                         reply_markup=ikb)
            except Exception as e:
                print(f"Exception while trying to edit reply markup: {e}")

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

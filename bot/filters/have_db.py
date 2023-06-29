from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from bot.utils.db_api import quick_commands as commands


class HaveInDb(BoundFilter):
    def __init__(self, consist):
        self.consist = consist

    async def check(self, message: types.Message):
        try:
            user = await commands.select_user(message)
            if user.status != 'active':
                # await message.answer(f'Вы ещё не зарегистрированы. \nДля регистрации нажмите /start')
                return self.consist
            else:
                # user = await commands.select_user(message.from_user.id)
                # return user.status is not 'active'
                return not self.consist
        except Exception:
            return True
        # return True

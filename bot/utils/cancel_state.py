from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.loader import bot

from bot.utils.db_api.schemes.user import User as SCHUser
from bot.utils.localization.i18n import MessageFormatter

from bot.keyboards.inline.inline_kb_default import ikb_default


async def cancel_func(message: types.Message, language: str, state: FSMContext,
                      state_mapping: dict, format_dict: dict, buttons: dict = None):
    current_state = await state.get_state()
    current_state_object = state_mapping.get(current_state)
    if current_state_object is not None:
        await bot.delete_message(message.from_user.id,
                                 current_state_object.message_id)
    await message.delete()

    await state.reset_state(with_data=False)
    await message.answer(
        text=MessageFormatter(language).get_message(format_dict=format_dict),
        reply_markup=ikb_default(language, buttons))

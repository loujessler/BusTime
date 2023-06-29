import asyncio

from aiogram import types

from bot.keyboards.inline.inline_kb_default import ikb_default
from bot.loader import dp, bot

from bot.handlers.main.bot_start import edit_ls

from bot.keyboards.inline.inline_kb_notification import make_keyboard

from bot.utils.localization.i18n import MessageFormatter


@dp.callback_query_handler(text='notification')
async def notification(call: types.CallbackQuery):
    user = call.conf.get('user')
    msg_locale = await bot.send_message(
        chat_id=call.message.chat.id,
        text=MessageFormatter(user.language, 'keyboards').get_message({'set_notification_time': 'none'}, None, 0),
        reply_markup=make_keyboard(user, 1, 30)
    )
    await call.message.edit_reply_markup(reply_markup=ikb_default(user.language, {
        'back_to_main_menu': f'back_to_main_menu:message_id:{msg_locale.message_id}',
    }))


@dp.callback_query_handler(text_startswith=['inc_minutes', 'dec_minutes', 'inc_seconds',
                                            'dec_seconds', 'set_notification'])
async def process_callback(call: types.CallbackQuery):
    user = call.conf.get('user')
    msg = MessageFormatter(user.language, 'keyboards')
    action, minutes, seconds = call.data.split(':')
    old_minutes = int(minutes)
    old_seconds = int(seconds)
    minutes = old_minutes
    seconds = old_seconds

    if action == 'inc_minutes':
        minutes += 1
    elif action == 'dec_minutes':
        minutes = max(0, old_minutes - 1)
    elif action == 'inc_seconds':
        seconds += 10
        if seconds >= 60:
            minutes += 1
            seconds -= 60
    elif action == 'dec_seconds':
        if seconds == 0:
            minutes = max(0, minutes - 1)
            seconds = 50
        else:
            seconds = max(0, old_seconds - 10)
    elif action == 'set_notification':
        if minutes == 0 and seconds == 0:
            await call.answer(msg.get_message({'error_set_notification': 'none'}, None, 0),
                              show_alert=True)
            return
        else:
            await edit_ls.edit_last_message(
                msg.get_message({'done_set_notification_time': 'none'},
                                {'minutes': minutes, 'seconds': seconds}, 0),
                call
            )
            await asyncio.sleep(minutes * 60 + seconds)
            await bot.send_message(call.message.chat.id,
                                   msg.get_message({'received_notification': 'none'},
                                                   None, 0),
                                   reply_markup=ikb_default(user.language))
            return

    if old_minutes != minutes or old_seconds != seconds:
        await call.message.edit_text(msg.get_message({'set_notification_time': 'none'}, None, 0),
                                     reply_markup=make_keyboard(user, minutes, seconds))

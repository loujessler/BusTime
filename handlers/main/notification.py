import asyncio

from aiogram import types

from keyboards.inline.inline_kb_default import ikb_default
from loader import dp, bot

from handlers.main.bot_start import edit_ls

from keyboards.inline.inline_kb_notification import make_keyboard

from utils.arrival import arrival
from utils.db_api import quick_commands as commands
from utils.i18n import MessageFormatter


@dp.callback_query_handler(text='notification')
async def notification(call: types.CallbackQuery):
    user = await commands.select_user(call.from_user.id)
    await call.message.edit_reply_markup(reply_markup=ikb_default(user, {
        'back_to_main_menu': 'back_to_main_menu',
    }))
    await bot.send_message(
        chat_id=call.message.chat.id,
        text=MessageFormatter(user.language).get_message({'set_notification_time': 'none'}, None, 0, 'keyboards'),
        reply_markup=make_keyboard(user, 1, 30)
    )


@dp.callback_query_handler(lambda c: c.data.startswith('inc_minutes') or
                                     c.data.startswith('dec_minutes') or
                                     c.data.startswith('inc_seconds') or
                                     c.data.startswith('dec_seconds') or
                                     c.data.startswith('set_notification'))
async def process_callback(call: types.CallbackQuery):
    user = await commands.select_user(call.from_user.id)
    msg = MessageFormatter(user.language)
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
        seconds += 5
        if seconds >= 60:
            minutes += 1
            seconds -= 60
    elif action == 'dec_seconds':
        if seconds == 0:
            minutes = max(0, minutes - 1)
            seconds = 55
        else:
            seconds = max(0, old_seconds - 5)
    elif action == 'set_notification':
        if minutes == 0 and seconds == 0:
            await call.answer(msg.get_message({'error_set_notification': 'none'}, None, 0, 'keyboards'),
                              show_alert=True)
            return
        else:
            await edit_ls.edit_last_message(
                msg.get_message({'done_set_notification_time': 'none'},
                                {'minutes': minutes, 'seconds': seconds}, 0, 'keyboards'),
                call,
                ikb_default(user)
            )
            await asyncio.sleep(minutes * 60 + seconds)
            await bot.send_message(call.message.chat.id,
                                   msg.get_message({'received_notification': 'none'},
                                                   None, 0, 'keyboards'),
                                   reply_markup=ikb_default(user))
            return

    if old_minutes != minutes or old_seconds != seconds:
        await call.message.edit_text(msg.get_message({'set_notification_time': 'none'}, None, 0, 'keyboards'),
                                     reply_markup=make_keyboard(user, minutes, seconds))

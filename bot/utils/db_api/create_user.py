from loguru import logger

from data.languages import languages
from bot.utils.db_api import quick_commands as commands


async def create_user(aio_type):
    user_data = {'user_id': aio_type.from_user.id,
                 'first_name': aio_type.from_user.first_name,
                 'last_name': aio_type.from_user.last_name,
                 'username': aio_type.from_user.username}

    language_code = aio_type.from_user.language_code
    if language_code not in languages:
        user_data['language'] = 'en'
    elif language_code == 'be':
        user_data['language'] = 'ru'
    else:
        user_data['language'] = language_code

    try:
        await commands.add_user(user_id=user_data['user_id'],
                                first_name=user_data['first_name'],
                                last_name=user_data['last_name'],
                                username=user_data['username'],
                                status='active',
                                language=user_data['language'])
        # LOGS
        logger.log(25, f"Created new user {user_data['user_id']}.")
    except Exception as e:
        # Here you can add logging or additional error handling
        raise e

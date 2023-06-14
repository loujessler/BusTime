import aiogram.utils.markdown as fmt


def language_mes(aio_type):
    text = fmt.text(
        f'✌️ Hi, {aio_type.from_user.first_name}.\n',
        fmt.hbold('🏳️ Choose your language: ')
    )
    return text

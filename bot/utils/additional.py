from aiogram import types
import base64


async def get_image_data(filepath):
    with open(filepath, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return "data:image/png;base64," + encoded_string


async def capitalize_words(sentence):
    words = sentence.split()
    capitalized_words = [word.capitalize() for word in words]
    return ' '.join(capitalized_words)


class ConvertNumber:
    def __init__(self, name_type: str):
        self.name_type = name_type
        self.type_dict = {
            'emoji_numbers': {
                '0': '0⃣',
                '1': '1⃣',
                '2': '2⃣',
                '3': '3⃣',
                '4': '4⃣',
                '5': '5⃣',
                '6': '6⃣',
                '7': '7⃣',
                '8': '8⃣',
                '9': '9⃣',
            },
            'forward_numbers': {
                '0': '🅰',
                '1': '🅱',
            }
        }

    def convert(self, number) -> str:
        result = ''
        for digit in str(number):
            result += self.type_dict[self.name_type].get(digit, digit)

        return result


def number_to_emoji(number):
    emoji_numbers = {
        '0': '0⃣',
        '1': '1⃣',
        '2': '2⃣',
        '3': '3⃣',
        '4': '4⃣',
        '5': '5⃣',
        '6': '6⃣',
        '7': '7⃣',
        '8': '8⃣',
        '9': '9⃣',
    }

    emoji_number = ''
    for digit in str(number):
        emoji_number += emoji_numbers.get(digit, digit)

    return emoji_number


async def return_msg_aio_type(aio_type):
    if isinstance(aio_type, types.CallbackQuery):
        return aio_type.message
    elif isinstance(aio_type, types.Message):
        return aio_type
    else:
        return  # Выход из функции, если передан некорректный объект

def number_to_emoji(number):
    emoji_numbers = {
        '0': '0️⃣',
        '1': '1️⃣',
        '2': '2️⃣',
        '3': '3️⃣',
        '4': '4️⃣',
        '5': '5️⃣',
        '6': '6️⃣',
        '7': '7️⃣',
        '8': '8️⃣',
        '9': '9️⃣',
    }

    emoji_number = ''
    for digit in str(number):
        emoji_number += emoji_numbers.get(digit, digit)

    return emoji_number

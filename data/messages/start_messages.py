import aiogram.utils.markdown as fmt


def language_mes(aio_type):
    text = fmt.text(
        f'✌️ Hi, {aio_type.from_user.first_name}.\n',
        fmt.hbold('🏳️ Choose your language: ')
    )
    return text


# def finish_registration(language):
#     translations = get_translations(language)
#     message = fmt.text(
#         fmt.hbold(translations.gettext('welcome_message')),
#         translations.gettext('instructions_message')
#     )
#     return message



# import aiogram.utils.markdown as fmt
# from utils.db_api import quick_commands as commands
#
#
# class Messages:
#     def __init__(self, user):
#         self.user = user
#
#     @staticmethod
#     def language_mes(aio_type):
#         text = fmt.text(
#             f'✌️ Hi, {aio_type.from_user.first_name}.\n',
#             fmt.hbold('🏳️ Choose your language: ')
#         )
#         return text
#
#     def finish_registration(self):
#         message = {
#             'ru': fmt.text(
#                 fmt.hbold('🌟🚌 Добро пожаловать в BUSTIME - сервис расписаний общественного транспорта в Тбилиси! 🚍🎉\n\n'),
#                 'Здесь вы можете получить актуальное расписание, указав номер остановки. 🔢\n'
#                 'Просто введите номер, и мы предоставим вам информацию о приближающихся автобусах. 📋\n\n'
#                 '😊💡 Вы также можете добавить заметки к интересующей вас остановке '
#                 'для удобного отслеживания информации о ней. Для этого выберите пункт "Мои остановки" (/my_bus_stops) '
#                 'в меню и введите название остановки и её ID. 📝'
#             ),
#             'en': fmt.text(
#                 fmt.hbold('🌟🚌 Welcome to BUSTIME - the public transport schedule service in Tbilisi! 🚍🎉\n\n'),
#                 'Here you can obtain the current schedule by specifying the bus stop number. 🔢\n'
#                 'Simply input the stop number, and we will provide you with information about the upcoming buses. 📋\n\n'
#                 '😊💡 You can also add notes to the bus stop you\'re interested in '
#                 'to conveniently track its information. To do this, select the "My Bus Stops" (/my_bus_stops) '
#                 'item in the menu, and then enter the stop\'s name and its ID. 📝'
#             ),
#             'ka': fmt.text(
#                 fmt.hbold('🌟🚌 მოგესალმებით BUSTIME-ში - საჯარო ტრანსპორტის განრიგის სერვისში თბილისში! 🚍🎉\n\n'),
#                 'აქ შეგიძლიათ მიიღოთ ამჟამინდელი განრიგი, მიუთითებლად გაჩერების ადგილის ნომერს. 🔢\n'
#                 'უბრალოდ შეიყვანეთ ნომერი და ჩვენ გამოგიგზავნით მოახლოებული ავტობუსების შესახებ ინფორმაციას. 📋\n\n'
#                 '😊💡 შეგიძლიათ ასევე დაამატოთ შენიშვნები გაჩერების ადგილზე, რომელიც თქვენ გაინტერესებთ, '
#                 'ისინის ინფორმაციის კომფორტული მენეჯმენტისთვის. ამისთვის, აირჩიეთ მენიუს "ჩემი გაჩერების ადგილები" ('
#                 '/my_bus_stops)'
#                 'პუნქტი და შემდეგ შეიყვანეთ გაჩერების ადგილის სახელი და მისი ID. 📝'
#             )
#         }
#         return message[self.user.language]

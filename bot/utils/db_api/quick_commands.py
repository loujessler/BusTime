import typing

from aiogram import types
from asyncpg import UniqueViolationError
from sqlalchemy import and_

from .create_user import create_user
from .schemes.user import User
from .schemes.bus_stops import BusStop
from .schemes.user_stops import UserStop


async def add_user(user_id: int,
                   first_name: str,
                   last_name: str,
                   username: str,
                   status: str,
                   language: str):
    try:
        user = User(user_id=user_id,
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    status=status,
                    language=language)
        await user.create()
    except UniqueViolationError:
        print('Пользователь не добавлен')


async def select_all_users() -> list:
    return await User.query.gino.all()


async def count_users() -> int:
    users = await select_all_users()
    return len(users)


async def select_user(
        aio_type: typing.Union[types.Message, types.CallbackQuery],
        user_id: str = None
) -> User:
    """
    Select user from database

    :param aio_type:
    :param user_id:
    :return:
    """
    user_id = user_id if user_id else aio_type.from_user.id
    user = await User.query.where(User.user_id == user_id).gino.first()
    if user is None:
        await create_user(aio_type)
        user = await User.query.where(User.user_id == user_id).gino.first()
    return user


async def update_status(
        aio_type: typing.Union[types.Message, types.CallbackQuery],
        status: str,
        user_id: str = None
):
    """
    Update status in database

    :param aio_type:
    :param status:
    :param user_id:
    :return:
    """
    user = await select_user(aio_type, user_id)
    await user.update(status=status).apply()


async def update_language(
        aio_type: typing.Union[types.Message, types.CallbackQuery],
        language: str
):
    """
    Update language in database

    :param aio_type:
    :param language:
    :return:
    """
    user = await select_user(aio_type)
    await user.update(language=language).apply()


# ----- BUS STOP -----

async def add_bus_stop(
        user: User,
        name: str,
        id_stop: int
):
    """
    Add new bus stop for user

    :param user:
    :param name:
    :param id_stop:
    :return:
    """
    try:
        bus_stop = await BusStop.query.where(and_(BusStop.name == name, BusStop.id_stop == id_stop)).gino.first()
        if not bus_stop:
            bus_stop = await BusStop.create(name=name, id_stop=id_stop)
        user_stop = UserStop(user_id=user.user_id, stop_id=bus_stop.id)
        await user_stop.create()
    except UniqueViolationError:
        print('Остановка не добавлена')


async def select_all_bus_stops(user: User) -> list:
    """
    Select all user's bus stops

    :param user:
    :return:
    """
    bus_stops = []
    try:
        user_stops = await UserStop.query.where(UserStop.user_id == user.user_id).gino.all()
        for user_stop in user_stops:
            bus_stop = await BusStop.query.where(BusStop.id == user_stop.stop_id).gino.first()
            bus_stops.append(bus_stop)
    except Exception as e:
        print(f"An error occurred: {e}")
    return bus_stops


async def select_bus_stop(user: User, id_unique: str) -> typing.Union[BusStop, None]:
    """
    Select user's bus stop

    :param user:
    :param id_unique:
    :return:
    """
    user_stop = await UserStop.query.where(
        (UserStop.user_id == user.user_id) & (UserStop.stop_id == id_unique)
    ).gino.first()
    if user_stop:
        return await BusStop.query.where(BusStop.id == user_stop.stop_id).gino.first()
    else:
        return None


async def delete_bus_stop(user: User, id_unique: str) -> bool:
    """
    Delete user's bus stop

    :param user:
    :param id_unique:
    :return:
    """
    user_stop = await UserStop.query.where(
        (UserStop.user_id == user.user_id) & (UserStop.stop_id == id_unique)
    ).gino.first()
    if user_stop:
        await user_stop.delete()
        return True
    else:
        return False


async def select_bus_stop_by_id(id_unique: str) -> BusStop:
    """
    Select user's bus stop by ID

    :param id_unique:
    :return:
    """
    return await BusStop.query.where(BusStop.id == id_unique).gino.first()


async def update_name_bus_stop(id_unique: str, name: str):
    """
    Update name user's bus stop

    :param id_unique:
    :param name:
    :return:
    """
    bus_stop = await select_bus_stop_by_id(id_unique)
    await bus_stop.update(name=name).apply()


async def update_code_bus_stop(id_unique: str, id_stop: str):
    """
    Update code user's bus stop

    :param id_unique:
    :param id_stop:
    :return:
    """
    bus_stop = await select_bus_stop_by_id(id_unique)
    await bus_stop.update(id_stop=id_stop).apply()

# async def add_bus_stop(user, name: str, id_stop: int):
#     try:
#         bus_stop = BusStop(name=name, id_stop=id_stop, user_id=user.user_id)
#         bus_stop.user = user
#         await bus_stop.create()
#     except UniqueViolationError:
#         print('Остановка не добавлена')
#
#
# async def select_all_bus_stops(user):
#     try:
#         bus_stops = await BusStop.query.where(BusStop.user_id == user.user_id).gino.all()
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         bus_stops = []
#     return bus_stops
#
#
# async def select_bus_stop(user, id_unique):
#     bus_stop = await BusStop.query.where(
#         (BusStop.user_id == user.user_id) & (BusStop.id == id_unique)
#     ).gino.first()
#     return bus_stop
#
#
# async def delete_bus_stop(user, id_unique):
#     bus_stop = await select_bus_stop(user, id_unique)
#     if bus_stop:
#         await bus_stop.delete()
#         return True
#     else:
#         return False
#
#
# async def select_bus_stop_by_id(id_unique):
#     bus_stop = await BusStop.query.where(BusStop.id == id_unique).gino.first()
#     return bus_stop
#
#
# async def update_name_bus_stop(id_unique, name):
#     bus_stop = await select_bus_stop_by_id(id_unique)
#     await bus_stop.update(name=name).apply()
#
#
# async def update_code_bus_stop(id_unique, id_stop):
#     bus_stop = await select_bus_stop_by_id(id_unique)
#     await bus_stop.update(id_stop=id_stop).apply()

from asyncpg import UniqueViolationError
from sqlalchemy import and_

from .create_user import create_user
from .db_gino import db
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


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def count_users():
    count = await db.func.count(User.user_id).gino.scalar()
    return count


async def select_user(aio_type, user_id=None):
    if user_id is not None:
        user = await User.query.where(User.user_id == user_id).gino.first()
    else:
        user = await User.query.where(User.user_id == aio_type.from_user.id).gino.first()
        if user is None:
            await create_user(aio_type)
            user = await User.query.where(User.user_id == aio_type.from_user.id).gino.first()
    return user


async def update_status(aio_type, status, user_id=None):
    user = await select_user(aio_type, user_id)
    await user.update(status=status).apply()


async def update_language(aio_type, language):
    user = await select_user(aio_type)
    await user.update(language=language).apply()


# ----- BUS STOP -----

async def add_bus_stop(user, name: str, id_stop: int):
    try:
        bus_stop = await BusStop.query.where(and_(BusStop.name == name, BusStop.id_stop == id_stop)).gino.first()
        if not bus_stop:
            bus_stop = await BusStop.create(name=name, id_stop=id_stop)
        user_stop = UserStop(user_id=user.user_id, stop_id=bus_stop.id)
        await user_stop.create()
    except UniqueViolationError:
        print('Остановка не добавлена')


async def select_all_bus_stops(user):
    try:
        user_stops = await UserStop.query.where(UserStop.user_id == user.user_id).gino.all()
        bus_stops = []
        for user_stop in user_stops:
            bus_stop = await BusStop.query.where(BusStop.id == user_stop.stop_id).gino.first()
            bus_stops.append(bus_stop)
    except Exception as e:
        print(f"An error occurred: {e}")
        bus_stops = []
    return bus_stops


async def select_bus_stop(user, id_unique):
    user_stop = await UserStop.query.where(
        (UserStop.user_id == user.user_id) & (UserStop.stop_id == id_unique)
    ).gino.first()
    if user_stop:
        return await BusStop.query.where(BusStop.id == user_stop.stop_id).gino.first()
    else:
        return None


async def delete_bus_stop(user, id_unique):
    user_stop = await UserStop.query.where(
        (UserStop.user_id == user.user_id) & (UserStop.stop_id == id_unique)
    ).gino.first()
    if user_stop:
        await user_stop.delete()
        return True
    else:
        return False


async def select_bus_stop_by_id(id_unique):
    bus_stop = await BusStop.query.where(BusStop.id == id_unique).gino.first()
    return bus_stop


async def update_name_bus_stop(id_unique, name):
    bus_stop = await select_bus_stop_by_id(id_unique)
    await bus_stop.update(name=name).apply()


async def update_code_bus_stop(id_unique, id_stop):
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

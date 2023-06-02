from asyncpg import UniqueViolationError

from utils.db_api.db_gino import db
from utils.db_api.schemes.user import User
from utils.db_api.schemes.bus_stops import BusStop


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


async def select_user(user_id):
    user = await User.query.where(User.user_id == user_id).gino.first()
    return user


async def update_status(user_id, status):
    user = await select_user(user_id)
    await user.update(status=status).apply()


async def update_language(user_id, language):
    user = await select_user(user_id)
    await user.update(language=language).apply()


async def add_bus_stop(user, name: str, id_stop: int):
    try:
        bus_stop = BusStop(name=name, id_stop=id_stop, user_id=user.user_id)
        bus_stop.user = user
        await bus_stop.create()
    except UniqueViolationError:
        print('Остановка не добавлена')


async def delete_bus_stop(user, name: str, id_stop: int):
    try:
        bus_stop = BusStop(name=name, id_stop=id_stop, user_id=user.user_id)
        bus_stop.user = user
        await bus_stop.create()
    except UniqueViolationError:
        print('Остановка не добавлена')


async def select_all_bus_stops(user):
    try:
        bus_stops = await BusStop.query.where(BusStop.user_id == user.user_id).gino.all()
    except Exception as e:
        print(f"An error occurred: {e}")
        bus_stops = []
    return bus_stops


async def select_bus_stop(user, id_unique):
    bus_stop = await BusStop.query.where(
        (BusStop.user_id == user.user_id) & (BusStop.id == id_unique)
    ).gino.first()
    return bus_stop


async def delete_bus_stop(user, id_unique):
    bus_stop = await select_bus_stop(user, id_unique)
    if bus_stop:
        await bus_stop.delete()
        return True
    else:
        return False


# async def add_bus_stop(user, name: str, id_stop: int):
#     try:
#         bus_stop = BusStop(name=name, id_stop=id_stop)
#         user.bus_stops.append(bus_stop)
#         await user.update().apply()
#         # user.update(bus_stops=bus_stop).apply()
#         # await bus_stop.create()
#     except UniqueViolationError:
#         print('Остановка не добавлена')


# async def select_all_bus_stops():
#     bus_stops = await BusStop.query.gino.all()
#     return bus_stops

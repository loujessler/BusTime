from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import select, insert
from sqlalchemy import Column, String, Integer, sql, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from data.config import POSTGRES_USER, POSTGRES_PASSWORD, ip, DATABASE

import asyncio
from .loader import db
from .utils.db_api.db_gino import TimedBaseModel
from .utils.db_api.schemes.bus_stops import BusStop
from .utils.db_api.schemes.user_stops import UserStop


class BusStopOld(TimedBaseModel):
    __tablename__ = 'bus_stops'

    id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    name = Column(String(200))
    id_stop = Column(Integer, primary_key=True)
    user = relationship('User', back_populates='bus_stops')
    user_id = Column(BigInteger, ForeignKey('users.user_id'))

    query: sql.select


async def migrate_data():
    # Подключись к базе данных
    await db.set_bind(f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{ip}/{DATABASE}')

    # Создай новую таблицу
    await UserStop.gino.create()

    # Получи все остановки
    bus_stops = await BusStopOld.query.gino.all()

    # Вставь данные в новую таблицу
    for bus_stop in bus_stops:
        user_stop = UserStop(user_id=bus_stop.user_id, stop_id=bus_stop.id)
        await user_stop.create()

    # Удали столбец 'user_id' из таблицы 'bus_stops'
    await db.status('ALTER TABLE bus_stops DROP COLUMN user_id')

    # Закрой подключение к базе данных
    await db.pop_bind().close()
    print("Migration DONE")

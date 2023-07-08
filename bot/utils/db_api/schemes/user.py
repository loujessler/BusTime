from sqlalchemy import Column, BigInteger, String, sql
from sqlalchemy.orm import relationship

from bot.utils.db_api.db_gino import TimedBaseModel
from bot.utils.db_api.schemes.user_stops_association import user_stops_association


class User(TimedBaseModel):
    __tablename__ = 'users'

    user_id = Column(BigInteger, primary_key=True, unique=True)
    first_name = Column(String(200))
    last_name = Column(String(200))
    username = Column(String(50))
    status = Column(String(30))
    language = Column(String(3))

    # Отношение "многие ко многим" с BusStop через ассоциативную таблицу
    bus_stops = relationship('BusStop', secondary=user_stops_association, back_populates='users')

    query: sql.select


# class User(TimedBaseModel):
#     __tablename__ = 'users'
#
#     user_id = Column(BigInteger, primary_key=True, unique=True)
#     first_name = Column(String(200))
#     last_name = Column(String(200))
#     username = Column(String(50))
#     status = Column(String(30))
#     language = Column(String(3), primary_key=True)
#
#     # Определяем отношение один-ко-многим с моделью BusStop
#     bus_stops = relationship('BusStop', back_populates='user')
#
#     query: sql.select

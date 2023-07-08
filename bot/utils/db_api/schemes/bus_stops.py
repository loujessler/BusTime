from sqlalchemy import Column, String, Integer, sql, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from bot.utils.db_api.db_gino import TimedBaseModel
from bot.utils.db_api.schemes.user_stops_association import user_stops_association


class BusStop(TimedBaseModel):
    __tablename__ = 'bus_stops'

    id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    name = Column(String(200))
    id_stop = Column(Integer, primary_key=True)

    # Отношение "многие ко многим" с User через ассоциативную таблицу
    users = relationship('User', secondary=user_stops_association, back_populates='bus_stops')

    query: sql.select


# class BusStop(TimedBaseModel):
#     __tablename__ = 'bus_stops'
#
#     id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
#     name = Column(String(200))
#     id_stop = Column(Integer, primary_key=True)
#     user = relationship('User', back_populates='bus_stops')
#     user_id = Column(BigInteger, ForeignKey('users.user_id'))
#
#     query: sql.select

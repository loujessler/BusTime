from sqlalchemy import Column, String, Integer, sql, Sequence
from sqlalchemy.orm import relationship

from bot.utils.db_api.db_gino import TimedBaseModel
from bot.utils.db_api.schemes.user_stops_association import user_stops_association


class BusStop(TimedBaseModel):
    __tablename__ = 'bus_stops'

    id = Column(Integer, Sequence('id_seq'), autoincrement=True, primary_key=True, unique=True)
    name = Column(String(200))
    id_stop = Column(Integer, Sequence('id_stop_seq'), primary_key=True)

    # Отношение "многие ко многим" с User через ассоциативную таблицу
    users = relationship('User', secondary=user_stops_association, back_populates='bus_stops')

    query: sql.select

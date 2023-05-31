from sqlalchemy import Column, BigInteger, String, Integer, sql, ForeignKey
from sqlalchemy.orm import relationship

from utils.db_api.db_gino import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'users'

    user_id = Column(BigInteger, primary_key=True, unique=True)
    first_name = Column(String(200))
    last_name = Column(String(200))
    username = Column(String(50))
    status = Column(String(30))
    language = Column(String(3), primary_key=True)

    # Определяем отношение один-ко-многим с моделью BusStop
    bus_stops = relationship('BusStop', back_populates='user')

    query: sql.select

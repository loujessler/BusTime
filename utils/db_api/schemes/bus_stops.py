from sqlalchemy import Column, String, Integer, sql, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from utils.db_api.db_gino import TimedBaseModel


class BusStop(TimedBaseModel):
    __tablename__ = 'bus_stops'

    id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    name = Column(String(200))
    id_stop = Column(Integer, primary_key=True)
    user = relationship('User', back_populates='bus_stops')
    user_id = Column(BigInteger, ForeignKey('users.user_id'))

    query: sql.select

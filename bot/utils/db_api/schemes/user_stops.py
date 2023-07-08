from sqlalchemy import Column, BigInteger, Integer, ForeignKey, sql

from bot.utils.db_api.db_gino import BaseModel


class UserStop(BaseModel):
    __tablename__ = 'user_stops'

    user_id = Column('user_id', BigInteger(), ForeignKey('users.user_id'), primary_key=True)
    stop_id = Column('stop_id', Integer(), ForeignKey('bus_stops.id'), primary_key=True)

    query: sql.select

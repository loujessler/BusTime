from sqlalchemy import Table, Column, Integer, ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Создаем ассоциативную таблицу для связи "многие ко многим"
user_stops_association = Table('user_stops', Base.metadata,
                               Column('user_id', BigInteger, ForeignKey('users.user_id')),
                               Column('stop_id', Integer, ForeignKey('bus_stops.id'))
                               )

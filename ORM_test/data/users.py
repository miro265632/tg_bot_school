import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm

class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String,
                              index=True, nullable=True)
    name=sqlalchemy.Column(sqlalchemy.String,
                              index=True, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String,
                              index=True, nullable=True)
    age= sqlalchemy.Column(sqlalchemy.String,
                              index=True, nullable=True)
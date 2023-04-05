import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Card(SqlAlchemyBase):
    __tablename__ = 'cards'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    imgs_src = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    briefly_title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    imgs_src_briefly = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
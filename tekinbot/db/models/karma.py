from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from tekinbot.db.models import TekinTableBase


class Karma(TekinTableBase):

    __tablename__ = 'karma'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    user = Column(String(255), unique=True)
    sent = Column(Integer)
    received = Column(Integer)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    Float,
    DateTime,
    Boolean
)

Base = declarative_base()

class Property(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    channel_id = Column(String, nullable=False)
    value = Column(String, nullable=True)

class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    channel_id = Column(String, nullable=False)

class Phrase(Base):
    __tablename__ = 'phrases'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    phrase = Column(String, nullable=False)

class Moderator(Base):
    # for some reason moderator > admin in this bot.............
    __tablename__ = 'moderators'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    username = Column(String, nullable=True)
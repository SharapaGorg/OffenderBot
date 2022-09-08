from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config import TOKEN 
from database import Base

###### APP ######

bot = Bot(TOKEN, parse_mode="html")
dp = Dispatcher(bot, storage=MemoryStorage())

###### DATABASE ######

engine = create_engine("sqlite:///database/base")
Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
from aiogram.types import *
from controller import dp
from database import *

@dp.message_handler(commands=['start'])
async def start(message : Message):
    await message.answer("Приветствую, жду не дождусь новых указаний!")

@dp.message_handler(commands=['settings'])
async def settings(message : Message):
    author = message.from_user.id

    groups = get_admins(user_id=author)

    markup = ReplyKeyboardMarkup()

@dp.message_handler()
async def echo(message : Message):
    chat = message.chat

    await message.answer(chat.title)

from aiogram.types import *
from controller import dp

@dp.message_handler(commands=['start'])
async def start(message : Message):
    await message.answer("Приветсвую, жду не дождусь новых указаний!")


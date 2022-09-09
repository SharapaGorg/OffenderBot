from email import message_from_binary_file
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import *
from controller import dp, bot
from database import *
from utils import *

@dp.message_handler(commands=['dictionary'])
async def moderate_dictionary(message : Message, state : FSMContext):
    await message.answer("Ты уверен, что ты модератор, гений?..")


async def check_moderator(moderator : User):
    pass
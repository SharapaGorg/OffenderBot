from email.message import Message
from aiogram.types import *
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from controller import bot, dp
from database import *

async def startup(message):
    suggesting_commands = [
        BotCommand("/help", description="Подсказка"),
        BotCommand("/settings", description="Настройки обзывательств")
    ]

    await bot.set_my_commands(suggesting_commands)

####### USABLE TOOLS #######

async def general_info(message : Message):
    author = message.from_user.id
    chat = message.chat
    me = await bot.get_me()

    return author, chat, me

async def callback_general_info(message : Message):
    author = message.from_user.id
    me = await bot.get_me()

    return author, me

####### CALLBACK FUNCTIONS #######

class Settings(StatesGroup):
    chat = State()
    username = State()

async def choose_channel(message : Message, chat : Chat):

    author, me = await callback_general_info(message)
    Settings.chat = chat
    
    # it works ONLY in direct chat
    await Settings.username.set()
    await bot.send_message(author, "Напиши ник человека (@something), которого хочешь закибербуллить")
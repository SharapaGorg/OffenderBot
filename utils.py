from email.message import Message
from aiogram.types import BotCommand
from controller import bot
from database import *

async def startup(message):
    suggesting_commands = [
        BotCommand("/help", description="Подсказка"),
        BotCommand("/settings", description="Настройки обзывательств")
    ]

    await bot.set_my_commands(suggesting_commands)

async def general_info(message : Message):
    author = message.from_user.id
    chat = message.chat
    me = await bot.get_me()

    return author, chat, me
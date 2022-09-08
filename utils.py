from aiogram.types import BotCommand
from controller import bot
from database import *

async def startup(message):
    suggesting_commands = [
        BotCommand("/help", description="Подсказка"),
        BotCommand("/settings", description="Настройки обзывательств")
    ]

    await bot.set_my_commands(suggesting_commands)
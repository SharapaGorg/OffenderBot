from aiogram.types import *
from random import choice

from controller import dp, bot
from database import *
from utils import *
from static import *

@dp.message_handler(content_types=['new_chat_members'])
async def join_event(message : Message):
    author, chat, me = await general_info(message)

    await message.answer("Здравствуй, новое мясо")

    add_admin(author, chat.id)

@dp.message_handler(content_types=['left_chat_member'])
async def leave_event(message : Message):
    author, chat, me = await general_info(message)

    try:
        await message.answer("Досвидули, тут тебя никто не ждет")
    except:
        # bot was kicked
        delete_admin(channel_id=chat.id)

@dp.message_handler(content_types=ContentType.TEXT)
async def check_chat_messages(message : Message):
    author, chat, me = await general_info(message)

    props = get_properties(chat.id, author)

    if chat.type == 'private' or not props:
        return

    name = props[0].value

    if name in NAMES:
       await bot.send_message(chat.id, choice(NAMES[name]))

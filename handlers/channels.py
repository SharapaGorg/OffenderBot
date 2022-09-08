from aiogram.types import *
from controller import dp, bot
from database import *
from utils import *

# new chat member event
@dp.message_handler(content_types=['new_chat_members'])
async def join_event(message : Message):
    author, chat, me = await general_info(message)

    await message.answer("Здравствуй, новое мясо")

    add_admin(author, chat.id)

# somebody left the chat
@dp.message_handler(content_types=['left_chat_member'])
async def leave_event(message : Message):
    author, chat, me = await general_info(message)

    try:
        await message.answer("Досвидули, тут тебя никто не ждет")
    except:
        # bot was kicked
        delete_admin(channel_id=chat.id)
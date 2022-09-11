from aiogram.types import *
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
import string
import random
import logger

from controller import bot, dp
from static import *
from database import *


async def startup(message):
    suggesting_commands = [
        BotCommand("/help", description="Подсказка"),
        BotCommand("/settings", description="Настройки обзывательств"),
        BotCommand("/dictionary", description="Изменить глобальный словарь")
    ]

    await bot.set_my_commands(suggesting_commands)

####### USABLE TOOLS #######

class Button(InlineKeyboardButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.callback_data = ''.join(random.choice(
            string.ascii_uppercase + string.digits) for _ in range(32))

    def onClick(self, coro, *args, **kwargs):
        try:
            @dp.callback_query_handler(lambda call: call.data == self.callback_data)
            def some_coro(call):
                return coro(call, *args, **kwargs)

        except Exception as e:
            logger.error(f'{coro} - handler exception --> {e}')


async def general_info(message: Message):
    author = message.from_user.id
    chat = message.chat
    me = await bot.get_me()

    return author, chat, me


async def callback_general_info(message: Message):
    author = message.from_user.id
    me = await bot.get_me()

    return author, me

####### CALLBACK FUNCTIONS #######


class Settings(StatesGroup):
    username = State()
    name = State()

class NewName(StatesGroup):
    name = State()
    phrase = State()

class NewPhrase(StatesGroup):
    phrase = State()

class AcceptAction(StatesGroup):
    answer = State()

async def choose_channel(message: Message, chat: Chat, state: FSMContext):
    author, me = await callback_general_info(message)
    content = SETTINGS_USERS + '\n\n'

    async with state.proxy() as data:
        data['chat'] = chat

    #### MARKUP SECTION ####
    markup = InlineKeyboardMarkup()

    add_button = Button("Добавить настройку")
    add_button.onClick(add_user)

    markup.add(add_button)
    #### END MARKUP SECTION ####

    props = get_properties(chat.id)
    if props:
        content += 'Вот кстати уже добавленные настройки:'

        for prop in props:
            try:
                user = (await bot.get_chat_member(chat.id, prop.user_id)).user
                preview = Button(user.username)
                edit = Button("Изменить")
                delete = Button("Удалить")

                preview.onClick(show_user, user, prop.value)
                edit.onClick(edit_user, user.id, chat.id)
                delete.onClick(delete_user, user.id, chat, state)

                markup.row(preview, edit, delete)

            except:
                # members has left chat
                continue

    else:
        content += 'Пока что у тебя нет никаких настроек'

    await bot.send_message(author, content, reply_markup=markup)


async def edit_user(message : Message, user_id : str, channel_id : str):
    await message.answer(DEV_WARNING)

async def show_user(message: Message, user: User, name : str):
    content = "Вот, что по нему есть:\n\n"
    content += f"Имя профиля: <b>{user.full_name}</b>\n"
    content += f"Ник профиля: <b>@{user.username}</b>\n"
    content += f"Указанное имя: <b>{name}</b>\n\n"

    await bot.send_message(message.from_user.id, content)

async def delete_user(message: Message, user_id: str, chat: Chat, state: FSMContext):
    delete_property(user_id, chat.id)
    
    await choose_channel(message, chat, state)


async def add_user(message: Message):
    author, me = await callback_general_info(message)

    await Settings.username.set()
    await bot.send_message(author, SETTINGS_ADD_USER)

async def add_new_phrase(message : Message):
    author = message.from_user

    await NewName.name.set()
    await bot.send_message(author.id, "Тогда введи имя, которое хочешь добавить")

async def add_phrase_by_name(message : Message, state : FSMContext, name : str):
    author = message.from_user

    async with state.proxy() as data:
        data['name'] = name

    await NewName.phrase.set()
    await bot.send_message(author.id, ADD_PHRASE)

async def remove_phrases_by_name(message : Message, name : str):
    author = message.from_user
    await bot.send_message(author.id, "Оке, удаляю")

async def accept_action(message : Message, coro, *args, **kwargs):
    author = message.from_user
    markup = InlineKeyboardMarkup()
    
    yes = Button("Да")
    no = Button("Нет")

    yes.onClick(accept, coro, *args, **kwargs)
    no.onClick(decline)

    markup.row(yes, no)

    await bot.send_message(author.id, "Уверен, что хочешь выполнить это действи?", reply_markup=markup)

async def accept(message : CallbackQuery, coro, *args, **kwargs):
    author = message.from_user
    await bot.send_message(author.id, "Принято")

    await coro(message, *args, **kwargs)

async def decline(message : CallbackQuery):
    author = message.from_user
    await bot.send_message(author.id, "Отклонено")
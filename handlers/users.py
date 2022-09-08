from aiogram.types import *
from controller import dp, bot
from database import *
import string, random
import logger
from utils import *

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

@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.answer("Приветствую, жду не дождусь новых указаний!")


@dp.message_handler(commands=['settings'])
async def settings(message: Message):
    author = message.from_user.id
    markup = InlineKeyboardMarkup()

    groups = get_admins(user_id=author)

    for group in groups:
        chat = await bot.get_chat(group.channel_id)

        button = Button(chat.title)
        button.onClick(choose_channel, chat)

        markup.add(button)

    await message.answer("Выбери чат, для которого хочешь поменять настройки", reply_markup=markup)

@dp.message_handler(state = Settings.username)
async def choose_user(message : Message, state : FSMContext):
    try:   
        user = await bot.get_chat_member(state.chat, message.text)
    except Exception as e:
        print(e)
        await message.answer("Не могу найти такого..")
        return
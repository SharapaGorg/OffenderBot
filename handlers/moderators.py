from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import *
from controller import dp, bot
from database import *
from utils import *


class AdminCheck(StatesGroup):
    password = State()


@dp.message_handler(commands=['dictionary'])
async def moderate_dictionary(message: Message, state: FSMContext):
    author, chat, me = await general_info(message)

    moders = get_moderators(author)

    if not moders:
        await bot.send_message(author, DECLINE_MODERATOR)
        await bot.send_message(author, "Ладно, если скажешь кодовое слово, пропущу")
        await AdminCheck.password.set()

        return

    markup = InlineKeyboardMarkup()

    add_button = Button("Добавить новое имя")
    add_button.onClick(add_new_phrase)

    markup.add(add_button)

    phrases = dict()
    for phrase in get_phrases():

        if phrases.get(phrase.name) is None:
            phrases[phrase.name] = 0

        phrases[phrase.name] += 1

    for phrase in phrases:
        button = Button(f"{phrase} ({phrases[phrase]})")
        button.onClick(add_phrase_by_name, state, phrase)

        markup.add(button)

    await bot.send_message(author, ACCEPT_MODERATOR, reply_markup=markup)


@dp.message_handler(state=AdminCheck.password)
async def login(message: Message, state: FSMContext):
    author = message.from_user
    if message.text != PASSWORD:
        await bot.send_message(author.id, "Закатай губу")
        return

    add_moderator(author.id, author.username)

    await state.finish()
    await bot.send_message(author.id, "Тебе повезло, прощаю на этот раз")


@dp.message_handler(state=NewName.name)
async def set_name(message: Message, state: FSMContext):
    author = message.from_user

    async with state.proxy() as data:
        data['name'] = message.text

    await NewName.next()
    await bot.send_message(author.id, ADD_PHRASE)


@dp.message_handler(state=NewName.phrase)
async def set_phrase(message: Message, state: FSMContext):
    author = message.from_user

    async with state.proxy() as data:
        data['phrase'] = message.text

        await state.finish()

        add_phrase(data['name'], data['phrase'])
        await bot.send_message(author.id, f"Замечательно, на имя <b>{data['name']}</b> записана фраза <b>{data['phrase']}</b>")

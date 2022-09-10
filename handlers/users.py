from aiogram.dispatcher.storage import FSMContext
from aiogram.types import *
from controller import dp, bot
from database import *
from utils import *


@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.answer("Приветствую, жду не дождусь новых указаний!")


@dp.message_handler(commands=['settings'])
async def settings(message: Message, state: FSMContext):
    author = message.from_user.id
    markup = InlineKeyboardMarkup()

    groups = get_admins(user_id=author)

    for group in groups:
        try:
            chat = await bot.get_chat(group.channel_id)
        except:
            continue

        button = Button(chat.title)
        button.onClick(choose_channel, chat=chat, state=state)
        markup.add(button)

    await message.answer("Выбери чат, для которого хочешь поменять настройки", reply_markup=markup)


@dp.message_handler(state=Settings.username)
async def choose_user(message: Message, state: FSMContext):
    try:
        user = message.forward_from

        async with state.proxy() as data:
            data['user'] = user

            member = (await bot.get_chat_member(data['chat'].id, user.id)).user

        content = "Умничка, я смог найти этого чела:\n\n"
        content += f"<b>{member.full_name}</b>\n"
        content += f"<b>@{member.username}</b>\n"
        content += f"<b>{member.id}</b>\n\n"
        content += 'Теперь напиши его имя в любой форме и расходимся'

        await Settings.next()
        await message.answer(content)

    except Exception as e:
        print(e)
        await message.answer(SETTINGS_CHOOSE_USER)
        return


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Settings.name)
async def add_new_user(message: Message, state: FSMContext):
    name = message.text

    async with state.proxy() as data:
        data['name'] = name

        channel_id, user_id, value = data['chat'].id, data['user'].id, data['name']

        # delete current properties about this user
        delete_property(user_id, channel_id)

        # update database
        add_property(user_id, channel_id, value)

    await state.finish()
    await message.answer(f"Так и запишу: <b>{message.text}</b>")

import json

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from keyboards import admin_start, admin_news

from utils import db
from config import channel_id
from create_bot import bot
from utils import ms_to_users, ms_to_channel, add_message


async def start_menu(message: types.Message):
    if f"{message.from_user.id}" == "ВАЩ ID":
        Admin_menu_img = open("media/Img/Admin_Page.png", "rb")
        await bot.send_photo(
            message.from_user.id,
            Admin_menu_img,
            caption="Админ меню:",
            reply_markup=admin_start,
        )
    else:
        print("Неправильный айди")
        await message.answer(f"Ваш id: {message.from_user.id}")


# КОМАНДЫ==================================================================
async def archive(message: types.Message):
    with open("dicts_files/news_dict.json") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items()):
        news = (
            f"<b>{v['Title']}\n</b>" f"{v['Time']}\n" f"<a href='{v['Url']}'>Читать</a>"
        )

        await bot.send_message(message.from_user.id, news)

    await message.answer("Сообщения закончились")


async def news_menu(message: types.Message):
    await message.answer("Выберете источник:", reply_markup=admin_news)


async def mailing(message: types.Message):
    await message.answer("Здравствуй, админ! Напиши сообщение для твоей рассылки")
    await ms_to_users.text.set()


async def get_usr_text(message: types.Message, state: FSMContext):
    users = db.get_users()

    text = f"{message.text}"
    await state.update_data(text=text)
    await message.answer(
        "Вот данные которые ты дал:\n"
        "Сообщение:\n" + text + "\n"
        "Будет отправлено в рассылку"
    )

    for row in users:
        try:
            await bot.send_message(row[0], text)
            if int(row[1]) != 1:
                db.set_active(row[0], 1)
        except:
            db.set_active(row[0], 0)
    message_for_log = f"Администратор @{message.from_user.username}({message.from_user.id}) в рассылку сообщение: {text}"
    add_message(message_for_log)
    print(message_for_log)
    await state.finish()


async def send_channel(message: types.Message):
    await message.answer("Здравствуй, админ! Напиши сообщение для поста в канал")
    await ms_to_channel.text.set()


async def get_chnl_text(message: types.Message, state: FSMContext):
    text = f"{message.text}"
    await state.update_data(text=text)
    await message.answer(
        "Вот данные которые ты дал:\n"
        "Сообщение:\n" + text + "\n"
        "Будет отправлено в канал"
    )
    await bot.send_message(channel_id, f"{text}")
    message_for_log = f"Администратор @{message.from_user.username}({message.from_user.id}) в канал сообщение: {text}"
    print(message_for_log)
    add_message(message_for_log)
    await state.finish()


# РЕГ ХЕНДЛЕРОВ==================================================================
def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(start_menu, commands="admin")
    dp.register_message_handler(news_menu, Text(equals="Отправить новости"))
    dp.register_message_handler(send_channel, Text(equals="Отправить в канал"))
    dp.register_message_handler(mailing, Text(equals="Рассылка"))
    dp.register_message_handler(get_usr_text, state=ms_to_users.text)
    dp.register_message_handler(get_chnl_text, state=ms_to_channel.text)
    dp.register_message_handler(archive, Text(equals="Архив"))

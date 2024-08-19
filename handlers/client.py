import json

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from keyboards import five_news_in_line
from Parse import main

from utils import db
from create_bot import dp, bot


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    if message.chat.type == "private":
        if not db.user_exists(message.from_user.id):
            db.add_user(message.from_user.id)
        Main_img = open("media/Img/Main_Page.png", "rb")
        start_buttons = ["Последние 5 новостей", "Обновить список новостей"]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*start_buttons)
        await bot.send_photo(
            message.from_user.id,
            Main_img,
            caption="Лента новостей",
            reply_markup=keyboard,
        )


@dp.message_handler(commands="помощь")
@dp.message_handler(commands="help")
async def help(message: types.Message):
    await message.answer("Команды\n" "/start - показать кнопки меню")


# =======================Inline_button Последние 5 новостей===========================


async def get_5_all(message: types.Message):
    await message.answer("Выберете источник новостей:", reply_markup=five_news_in_line)


@dp.callback_query_handler(text="ria5")
async def get_5_ria(callback: types.callback_query):
    with open("dicts_files/rio_dict.json") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-5:]:
        news = (
            f"<b>{v['Title']}\n</b>" f"{v['Time']}\n" f"<a href='{v['Url']}'>Читать</a>"
        )
        await callback.message.answer(news)


@dp.callback_query_handler(text="ria_tr5")
async def get_5_ria_tr(callback: types.callback_query):
    with open("dicts_files/rio_Turkey_dict.json") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-5:]:
        news = (
            f"<b>{v['Title']}\n</b>" f"{v['Time']}\n" f"<a href='{v['Url']}'>Читать</a>"
        )
        await callback.message.answer(news)


@dp.callback_query_handler(text="seclab_news5")
async def get_5_seclab_news(callback: types.callback_query):
    with open("dicts_files/news_dict.json") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-5:]:
        news = (
            f"<b>{v['Title']}\n</b>"
            f"<i>{v['Desc']}\n</i>"
            f"{v['Time']}\n"
            f"<a href='{v['Url']}'>Читать</a>"
        )

        await callback.message.answer(news)


@dp.callback_query_handler(text="freesteam5")
async def get_5_freesteam(callback: types.callback_query):
    with open("dicts_files/games_sales.json") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-10:]:
        news = (
            f"<b>{v['News']}\n</b>"
            f"<i>{v['Tags']}\n</i>"
            f"{v['Time']}\n"
            f"<a href='{v['Url']}\n'>Читать</a>"
        )

        await callback.message.answer(news)


# =============================Другое=============================


async def get_fresh_news(message: types.Message):
    await message.answer("Обновляю...")
    main()
    await message.answer("Список новостей успешно обновлён")
    # fresh_news = SecurityLab_update()
    #
    # if len(fresh_news) >= 1:
    #     for k, v in sorted(fresh_news.Container()):
    #         admin_news = (
    #             f"<b>{v['article_title']}\n</b>"
    #             f"<a href='{v['article_url']}'>Читать</a>"
    #         )
    #         # f"<i>{v['article_desc']}\n</i>" \
    #
    #         SecurityLab_update()
    #
    #         await message.answer(admin_news)
    #
    # else:
    #     await message.answer("Пока нет свежих новостей...")


def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(start, commands="start")
    dp.register_message_handler(get_5_all, Text(equals="Последние 5 новостей"))
    dp.register_message_handler(get_5_ria, text="ria5")
    dp.register_message_handler(get_5_ria_tr, text="ria_tr5")
    dp.register_message_handler(get_5_seclab_news, text="seclab_news5")
    dp.register_message_handler(get_5_freesteam, text="freesteam5")
    dp.register_message_handler(get_fresh_news, Text(equals="Обновить список новостей"))

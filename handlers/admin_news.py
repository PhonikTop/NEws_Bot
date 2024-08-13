import json

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from config import channel_id
from create_bot import dp, bot


@dp.callback_query_handler(Text(equals="Риа Новости"))
async def send_5_ria(message: types.Message):
    with open("dicts_files/rio_dict.json") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-5:]:
        news = (
            f"<b>{v['Title']}\n</b>" f"<a href='{v['Url']}'>Читать</a>"
        )
        await bot.send_message(channel_id, news)

    await message.answer("Новости отправлены")
@dp.callback_query_handler(Text(equals="Риа Новости Турция"))
async def send_5_ria_tr(message: types.Message):
    with open("dicts_files/rio_Turkey_dict.json") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-5:]:
        news = (
            f"<b>{v['Title']}\n</b>" f"{v['Time']}\n" f"<a href='{v['Url']}'>Читать</a>"
        )
        await bot.send_message(channel_id, news)

    await message.answer("Новости отправлены")
@dp.callback_query_handler(Text(equals="Security Lab News"))
async def send_5_seclab_news(message: types.Message):
    with open("dicts_files/news_dict.json") as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-5:]:
        news = (
            f"<b>{v['Title']}\n</b>"
            f"{v['Time']}\n"
            f"<a href='{v['Url']}'>Читать</a>"
        )

        await bot.send_message(channel_id, news)

    await message.answer("Новости отправлены")

def register_handler_admin_news(dp: Dispatcher):
    dp.register_message_handler(send_5_ria, Text(equals="Риа Новости"))
    dp.register_message_handler(send_5_ria_tr, Text(equals="Риа Новости Турция"))
    dp.register_message_handler(send_5_seclab_news, Text(equals="Security Lab News"))

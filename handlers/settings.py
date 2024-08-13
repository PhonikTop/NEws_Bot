from aiogram import types, Dispatcher, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from create_bot import dp, bot


async def news_type_select(callback: types.callback_query):
    await callback.message.answer(
        "Выберите вид отправляемых новостей",
        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(
            KeyboardButton(text="Вариант 1"),
            KeyboardButton(text="Вариант 2"),
        ),
    )


def register_settings(dp: Dispatcher):
    dp.callback_query(news_type_select, F.text == "News_type_select")

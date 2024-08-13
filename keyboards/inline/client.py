from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


five_news_in_line = InlineKeyboardMarkup(row_width=2)

five_Freesteam = InlineKeyboardButton(text="Раздачи игр", callback_data="freesteam5")
five_ria = InlineKeyboardButton(text="Риа Новости", callback_data="ria5")
five_Turkey_ria = InlineKeyboardButton(
    text="Риа Новости Турция", callback_data="ria_tr5"
)
five_seclab = InlineKeyboardButton(
    text="Секьюрити лаб Новости", callback_data="seclab_news5"
)

five_news_in_line.add(five_ria, five_Turkey_ria, five_seclab, five_Freesteam)

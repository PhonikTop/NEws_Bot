from aiogram import types

# Неймы кнопок
start_buttons = ["Отправить в канал", "Рассылка", "Отправить новости", "Архив"]
news_buttons = ["Риа Новости", "Риа Новости Турция", "Security Lab News", "Назад"]

# Макапы
admin_start = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
admin_news = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

# Адды
admin_start.add(*start_buttons)
admin_news.add(*news_buttons)

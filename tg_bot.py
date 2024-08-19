from handlers import (
    register_handler_client,
    register_handler_admin,
    register_handler_admin_news,
)
from aiogram import executor
from create_bot import dp, storage, bot

from utils import add_message

register_handler_client(dp)
register_handler_admin(dp)
register_handler_admin_news(dp)


async def shutdown(dp):
    add_message("Бот неактивен")
    await storage.close()
    await bot.close()


async def startup(dp):
    add_message("Бот активен")


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=startup, on_shutdown=shutdown)

from aiogram.dispatcher.filters.state import StatesGroup, State


class ms_to_users(StatesGroup):
    text = State()
    time = State()


class ms_to_channel(StatesGroup):
    text = State()
    time = State()

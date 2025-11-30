from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_menu():
    builder = InlineKeyboardBuilder()

    builder.button(text="Подобрать смартфон", callback_data="menu:recommend")
    builder.button(text="Сравнить смартфоны", callback_data="menu:compare")
    builder.button(text="Помощь", callback_data="menu:help")

    builder.adjust(2, 1)

    return builder.as_markup()


def get_smartphone_menu():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Начать подбор",
        callback_data="smartphone:start_recommend"
        )
    builder.button(
        text="Популярные модели",
        callback_data="smartphone:popular"
    )
    builder.button(
        text="Назад в меню",
        callback_data="menu:main"
    )

    builder.adjust(1)

    return builder.as_markup()


def get_back_button():
    builder = InlineKeyboardBuilder()

    builder.button(text="Назад", callback_data="menu:main")

    return builder.as_markup()

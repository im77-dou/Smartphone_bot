from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_main_keyboard():
    builder = ReplyKeyboardBuilder()

    builder.button(text="Подобрать смартфон")
    builder.button(text="Сравнить смартфоны")
    builder.button(text="Помощь")

    builder.adjust(2, 1)

    return builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Выберите действие..."
    )


def get_cancel_keyboard():
    builder = ReplyKeyboardBuilder()

    builder.button(text="Отменить")

    return builder.as_markup(resize_keyboard=True)

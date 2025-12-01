from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from bot.keyboards.inline import get_main_menu, get_settings_menu

from utils.validators import is_valid_budget, extract_budget_from_text

import logging

logger = logging.getLogger(__name__)


router = Router(name="user")


@router.message(CommandStart())
async def cmd_start(message: Message):

    logger.info(
        f"User {message.from_user.id} @{message.from_user.username}"
        f"started the bot."
    )

    await message.answer(
        f"Привет, <b>{message.from_user.first_name}</b>!",
        reply_markup=get_main_menu()
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "<b>Доступные команды:</b>\n"
        "<code>/start</code> - Запустить бота\n"
        "<code>/help</code> - Справка по командам\n"
        "<code>/menu</code> - Главное меню\n"
        "<code>/cancel</code> - Отменить текущее действие\n"
        "<code>/compare</code> - Сравнить смартфоны\n"
        "<code>/recommend</code> - Подобрать смартфон\n"
        "<code>/settings</code> - Настройки\n"
        "<b>Общение:</b>\n"
        "Просто напишите сообщение, и я помогу вам."
    )


@router.message(Command("cancel"))
async def cmd_cancel(message: Message):
    await message.answer("Операция отменена.")


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer(
        "<b>Главное меню:</b>\n\n"
        "Выберите действие:",
        reply_markup=get_main_menu()
    )


@router.message(Command("settings"))
async def cmd_settings(message: Message):
    logger.info(f"User {message.from_user.id} requested settings.")

    await message.answer(
        "<b>Настройки:</b>\n\n"
        "Выберите действие:",
        reply_markup=get_settings_menu()
    )


@router.message(F.text == "Подобрать смартфон")
async def on_recommend_button(message: Message):
    await message.answer("Подобрать смартфон...")


@router.message(F.text == "Сравнить смартфоны")
async def on_compare_button(message: Message):
    await message.answer("Сравнить смартфоны...")


@router.message(F.text == "Помощь")
async def on_help_button(message: Message):
    await cmd_help(message)


@router.message(F.photo)
async def on_photo(message: Message):
    logger.info(f"User {message.from_user.id} sent a photo.")

    await message.answer(
        "<b>Фото получено.</b>\n\n"
        "Функция не реализована. Пока что."
    )


@router.message(F.voice)
async def on_voice(message: Message):
    logger.info(f"User {message.from_user.id} sent a voice message.")

    await message.answer(
        "<b>Голосовое сообщение получено.</b>\n\n"
        "Функция не реализована. Пока что."
    )


@router.message(F.text.startswith("/"))
async def unknown_command(message: Message):
    logger.warning(f"User @{message.from_user.id} typed unknown command: {message.text}")

    await message.answer(
        f"Неизвестная команда: {message.text}\n\n"
        f"Пожалуйста, используйте команду /help для получения справки."
    )


@router.message(F.text)
async def on_text_message(message: Message):
    logger.info(f"User @{message.from_user.username} said: {message.text}")

    budget = extract_budget_from_text(message.text)

    if budget:
        await message.answer(
            f"Ваш бюджет: <b>{budget}</b>$\n\n"
            f"Используйте /recommend для подбора смартфона."
        )
        return

    brands = [
        "apple", "iphone",
        "samsung", "galaxy",
        "google", "pixel",
        "xiaomi", "redmi", "mi", "poco",
        "huawei",
        "honor",
        "vivo", "iqoo",
        "oppo", "oneplus", "realme",
        "sony", "nokia",
        "motorola", "nubia", "zte",
        "inoi", "meizu", "cubot",
        "infinix", "tecno", "tcl", "nothing",
        "blackview", "htc", "red magic", "oukitel", "ulefone"
    ]
    mentioned_brands = [brand for brand in brands if brand in message.text.lower()]
    if mentioned_brands:
        brands_text = ", ".join(b.title() for b in mentioned_brands)
        await message.answer(
            f"Интересуетесь <b>{brands_text}</b>?\n\n"
            f"Используйте /recommend для подбора смартфона этого бренда."
        )
        return

    await message.answer(
        f"Получил ваше сообщение: {message.text[:100]}"
        f"Пока что я не умею обрабатывать текстовые сообщения."
    )

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from bot.keyboards.inline import get_main_menu, get_settings_menu

from utils.error_handler import handle_errors
from utils.messages import Messages

import logging

logger = logging.getLogger(__name__)

router = Router(name="user")


@router.message(CommandStart())
@handle_errors
async def cmd_start(message: Message):

    logger.info(
        f"User {message.from_user.id} @{message.from_user.username}"
        f"started the bot."
    )

    user_name = message.from_user.first_name
    await message.answer(
        Messages.welcome_user(user_name),
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
    await message.answer(Messages.INFO_CANCELED)


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


@router.message(F.text.startswith("/"))
async def unknown_command(message: Message):
    logger.warning(
        f"User @{message.from_user.id} "
        f"typed unknown command: {message.text}")

    await message.answer(
        f"Неизвестная команда: {message.text}\n\n"
        f"Пожалуйста, используйте команду /help для получения справки."
    )


@router.message(F.text)
async def on_text_message(message: Message):
    logger.info(f"User @{message.from_user.username} said: {message.text}")

    await message.answer(
        "<b>Пока что заглушка</b>"
    )

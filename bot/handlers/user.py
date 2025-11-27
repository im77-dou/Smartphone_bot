from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

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
        f"Привет, <b>{message.from_user.first_name}</b>!"
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "<b>Доступные команды:</b>\n"
        "<code>/start</code> - Запустить бота\n"
        "<code>/help</code> - Справка по командам\n"
        "<code>/cancel</code> - Отменить текущее действие\n"
        "<code>/compare</code> - Сравнить смартфоны\n"
        "<code>/recommend</code> - Подобрать смартфон\n"
        "<b>Общение:</b>\n"
        "Просто напишите сообщение, и я помогу вам."
    )


@router.message(Command("cancel"))
async def cmd_cancel(message: Message):
    await message.answer("Операция отменена.")


@router.message(F.text)
async def on_text_message(message: Message):

    logger.info(f"User @{message.from_user.username} said: {message.text}")

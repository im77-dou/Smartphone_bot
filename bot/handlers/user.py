from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message


router = Router(name="user")


@router.message(CommandStart())
async def cmd_start(message: Message):
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
        "<b>Общение:</b>\n"
        "Просто напишите сообщение, и я помогу вам."
    )

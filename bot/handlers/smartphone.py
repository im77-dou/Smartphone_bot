import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


logger = logging.getLogger(__name__)

router = Router(name="smartphone")


@router.message(Command("recommend"))
async def cmd_recommend(message: Message):
    logger.info(f"User @{message.from_user.id} requested recommendation.")


@router.message(Command("compare"))
async def cmd_compare(message: Message):
    logger.info(f"User @{message.from_user.id} requested compare.")

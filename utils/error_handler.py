import logging
from functools import wraps
from typing import Callable, Any

from aiogram.types import Message, CallbackQuery

logger = logging.getLogger(__name__)


def handle_errors(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(
                f"Error in {func.__name__}: {type(e).__name__}: {e}",
                exc_info=True
            )

            for arg in args:
                if isinstance(arg, Message):
                    await arg.answer(
                        "<b>Произошла ошибка.</b>\n\n"
                        "Попробуйте позже.\n"
                        "Если ошибка повторится, обратитесь в поддержку."
                    )
                    break
                elif isinstance(arg, CallbackQuery):
                    await arg.answer(
                        "Произошла ошибка. Попробуйте позже.",
                        show_alert=True
                    )
                    break

    return wrapper


async def log_message_details(message: Message):
    logger.debug(
        f"Message details:\n"
        f"  User ID: {message.from_user.id}\n"
        f"  Username: @{message.from_user.username}\n"
        f"  Chat ID: {message.chat.id}\n"
        f"  Text: {message.text[:100] if message.text else 'N/A'}\n"
        f"  Content type: {message.content_type}\n"
        f"  Date: {message.date}"
    )


async def log_callback_details(callback: CallbackQuery):
    logger.debug(
        f"Callback details:\n"
        f"  User ID: {callback.from_user.id}\n"
        f"  Username: @{callback.from_user.username}\n"
        f"  Callback data: {callback.data}\n"
        f"  Message ID: {callback.message.message_id if callback.message else 'N/A'}"
    )

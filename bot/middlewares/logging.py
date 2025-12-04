import logging
import time
from typing import Callable, Dict, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery


logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ):
        start_time = time.time()

        if isinstance(event, Message):
            event_type = "Message"
            user = event.from_user
            details = f"'{event.text[:50] if event.text else 'no text'}'"
        elif isinstance(event, CallbackQuery):
            event_type = "Callback"
            user = event.from_user
            details = f"data ='{event.data}'"
        else:
            event_type = "Unknown"
            user = None
            details = ""

        if user:
            logger.info(
                f"{event_type} from user {user.id} "
                f"@({user.username}): {details}"
            )
        try:
            result = await handler(event, data)
        except Exception as e:
            logger.error(
                f"Error proccesing {event_type}: {type(e).__name__}: {e}",
                exc_info=True
            )
            try:
                if isinstance(event, Message):
                    await event.answer(
                        "<b>Произошла ошибка</b>\n\n"
                        "Попробуйте еще раз или используйте /help"
                    )
                elif isinstance(event, CallbackQuery):
                    await event.answer(
                        "Произошла ошибка. Попробуйте еще раз.",
                        show_alert=True
                    )
            except Exception:
                pass

            raise
        procces_time = time.time() - start_time
        logger.info(f"Processed in {procces_time:.3f}s")

        return result

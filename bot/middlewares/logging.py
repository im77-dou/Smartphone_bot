import logging
import time
from typing import Callable, Dict, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import Message


logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ):

        user = event.from_user

        logger.info(
            f"Message from user: {user.id}, @{user.username}"
            f"'{event.text[:50] if event.text else 'no text'}'"
        )

        start_time = time.time()
        result = await handler(event, data)
        process_time = time.time() - start_time
        logger.info(f"Proccesed in {process_time:.3f}s")

        return result

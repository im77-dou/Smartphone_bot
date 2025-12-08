import logging
from typing import Callable, Dict, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.fsm.context import FSMContext

logger = logging.getLogger(__name__)


class FSMLoggingMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ):
        state: FSMContext = data.get("state")

        if state:
            current_state = await state.get_state()
            state_data = await state.get_data()

            user = getattr(event, "from_user", None)
            user_id = user.id if user else "unknown"

            if current_state:
                logger.debug(
                    f"[FSM] User {user_id} | State: {current_state} | "
                    f"Data keys: {list(state_data.keys())}"
                )

            result = await handler(event, data)
            new_state = await state.get_state()

            if current_state != new_state:
                logger.info(
                    f"[FSM TRANSITION] User {user_id} | "
                    f"{current_state or 'None'} -> {new_state or 'None'}"
                )

            return result

        return await handler(event, data)

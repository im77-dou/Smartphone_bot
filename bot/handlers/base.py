import logging
from aiogram.types import Message, CallbackQuery

logger = logging.getLogger(__name__)


async def safe_delete_message(message: Message):
    try:
        await message.delete()
        return True
    except Exception as e:
        logger.warning(f"Failed to delete message: {e}")
        return False


async def safe_answer_callback(
        callback: CallbackQuery,
        text: str = "",
        show_alert: bool = False
):
    try:
        await callback.answer(text, show_alert=show_alert)
        return True
    except Exception as e:
        logger.warning(f"Failed to answer callback: {e}")
        return False


async def safe_edit_message(
        callback: CallbackQuery,
        text: str,
        reply_markup=None
):
    try:
        await callback.message.edit_text(text, reply_markup=reply_markup)
        return True
    except Exception as e:
        logger.warning(f"Failed to edit message: {e}")
        return False

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import config
from bot.handlers import user


def setup_logging():
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL.upper(), logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


async def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        config.validate()
        logger.info("Configuration is valid.")
    except ValueError as e:
        logger.error(f"Error: {e}")
        return

    logger.info("Starting bot...")

    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()
    dp.include_router(user.router)

    logger.info("Bot started.")

    try:
        await dp.start_polling(bot)
    finally:
        logger.info("Bot stopping...")
        await bot.session.close()
        logger.info("Bot stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
    except Exception as e:
        print(f"\nError: {e}")
        raise

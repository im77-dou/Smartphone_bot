import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from config import config

from bot.handlers import user, smartphone

from bot.middlewares.logging import LoggingMiddleware


def setup_logging():
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL.upper(), logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


async def set_bot_commands(bot: Bot):
    logger = logging.getLogger(__name__)

    commands = [
        BotCommand(command="/start", description="Запустить бота"),
        BotCommand(command="/help", description="Справка по командам"),
        BotCommand(command="/cancel", description="Отменить действие"),
        BotCommand(command="/compare", description="Сравнить смартфоны"),
        BotCommand(command="/recommend", description="Подобрать смартфон")
    ]
    await bot.set_my_commands(commands)

    logger.info("Bot commands set.")


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
    await set_bot_commands(bot)

    dp.message.middleware(LoggingMiddleware())
    dp.include_router(user.router)
    dp.include_router(smartphone.router)

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

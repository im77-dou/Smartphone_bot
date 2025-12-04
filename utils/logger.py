import logging
import sys
from pathlib import Path


def setup_logger(
        name: str = __name__,
        level: int = logging.INFO,
        log_to_file: bool = True
):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
        )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_to_file:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        file_handler = logging.FileHandler(
            log_dir / "bot.log",
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

import os
from dotenv import load_dotenv


load_dotenv()


class Config:

    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")

    OPENAI_API_KEY: str = os.getenv("OPENAO_API_KEY", "")

    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "smartphone_bot")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
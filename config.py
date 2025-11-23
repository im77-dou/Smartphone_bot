import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    # tg bot
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")

    # openai
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    # database
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "smartphone_bot")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")

    @property
    def database_url(self):
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    # environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # level logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # validation
    def validate(self):
        errors = []

        if not self.BOT_TOKEN:
            errors.append("BOT_TOKEN is not set")
        if not self.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is not set")
        if not self.DB_PASSWORD:
            errors.append("DB_PASSWORD is not set")

        if errors:
            error_message = "\n".join(errors)
            raise ValueError(
                f"Configuration validation failed:\n{error_message}\n\n"
                "Please check your environment variables and try again."
            )


config = Config()


if __name__ == "__main__":
    try:
        config.validate()
        print("Configuration is valid.")
        print(f"Bot Token: {config.BOT_TOKEN[:10]}...")
        print(f"OpenAI API Key: {config.OPENAI_API_KEY[:10]}...")
        print(f"Database: {config.DB_NAME}")
        print(f"Environment: {config.ENVIRONMENT}")
    except ValueError as e:
        print(f"Error: {e}")

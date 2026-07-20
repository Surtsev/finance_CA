from typing import Optional

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "administrator"
    DB_NAME: str = "finance"
    DATABASE_URL: Optional[str] = None

    @computed_field  # type: ignore[prop-decorator]
    @property
    def database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@localhost:5433/{self.DB_NAME}"

    # Redis
    REDIS_URL: str = "redis://localhost:6380/0"

    # Telegram client, bot
    TELEGRAM_API_HASH: str = ""
    TELEGRAM_API_ID: str = ""
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_SESSION_NAME: str = "finance_bot"

    # App
    DEBUG: bool = False


settings = Settings()

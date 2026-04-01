from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения."""

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5433/finance"

    # Redis
    REDIS_URL: str = "redis://localhost:6380/0"

    # App
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()

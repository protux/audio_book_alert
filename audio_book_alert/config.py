from functools import lru_cache

from pydantic import (
    BaseSettings,
    Field,
)


class Settings(BaseSettings):
    telegram_bot_name: str = Field(..., env="ABA_TELEGRAM_BOT_NAME")
    telegram_api_key: str = Field(..., env="ABA_TELEGRAM_API_KEY")

    activate_database: bool = Field(default=False, env="ABA_ACTIVATE_DATABASE")
    database_url: str = Field(..., env="ABA_DATABASE_URL", description="Database Connection String")
    database_schema: str = Field(default=None, env="ABA_DATABASE_SCHEMA", description="Database Schema")


@lru_cache()
def get_settings():
    return Settings()

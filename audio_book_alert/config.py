from pydantic import (
    BaseSettings,
    Field,
)


class Settings(BaseSettings):
    telegram_bot_name: str = Field(..., env="ABA_TELEGRAM_BOT_NAME")
    telegram_api_key: str = Field(..., env="ABA_TELEGRAM_API_KEY")

    activate_database: bool = Field(..., env="ABA_ACTIVATE_DATABASE", default=False)

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class BotConfig(BaseModel):
    token: str


class ApiConfig(BaseSettings):
    base_url: str = "http://0.0.0.0:8000/api/v1"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )

    bot: BotConfig
    api: ApiConfig = ApiConfig()


settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, AmqpDsn
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class BotConfig(BaseModel):
    token: str


class ApiConfig(BaseSettings):
    base_url: str = "http://0.0.0.0:8000/api/v1"


class FastStreamConfig(BaseModel):
    rabbit_url: AmqpDsn = "amqp://guest:guest@localhost:5672/"
    tg_api_secret: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )

    bot: BotConfig
    api: ApiConfig = ApiConfig()
    fs: FastStreamConfig


settings = Settings()

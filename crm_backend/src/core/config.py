from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from typing import ClassVar
from pathlib import Path
from datetime import time, timedelta


BASE_DIR = Path(__file__).resolve().parent.parent


class APIPrefix(BaseModel):
    api_v1: str = "/api/v1"
    users: str = "/users"
    auth: str = "/auth"
    employees: str = "/employees"
    positions: str = "/positions"
    categories: str = "/categories"
    services: str = "/services"
    booking: str = "/booking"


class DBConfig(BaseModel):
    naming_convention: ClassVar[dict] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str
    postgres_db: str
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 5
    max_overflow: int = 10

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@"
            f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


class MiddlewareConfig(BaseModel):
    cors_allowed_origins: list[str]


class AUTHConfig(BaseModel):
    secret_key: str
    access_expire_day: int
    refresh_expire_day: int
    algorithm: str = "HS256"


class BookingConfig(BaseModel):
    work_start: time = time(9, 0)
    work_end: time = time(18, 0)
    buffer: timedelta = timedelta(minutes=15)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    db: DBConfig
    midd: MiddlewareConfig
    jwt: AUTHConfig
    api_prefix: APIPrefix = APIPrefix()
    booking: BookingConfig = BookingConfig()


settings = Settings()

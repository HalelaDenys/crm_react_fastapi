from faststream.rabbit import RabbitBroker
from core import settings
from faststream import FastStream
from infrastructure.fs_broker.router.tg_user_router import tg_user_router

# ініціалізація брокера
broker = RabbitBroker(
    settings.fs.rabbit_url,
)

# створюємо FastStream app
fs_app = FastStream(broker)

# підключаємо маршрутизатор до app
broker.include_router(tg_user_router)

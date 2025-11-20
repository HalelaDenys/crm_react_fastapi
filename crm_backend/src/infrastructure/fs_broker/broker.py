from faststream.rabbit import RabbitBroker
from core import settings
from faststream import FastStream


# ініціалізація брокера
broker = RabbitBroker(
    settings.fs.rabbit_url,
)

# створюємо FastStream app
fs_app = FastStream(broker)

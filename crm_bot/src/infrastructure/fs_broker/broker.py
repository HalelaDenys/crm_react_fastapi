from faststream.rabbit import RabbitBroker
from faststream import FastStream
from core import settings
from infrastructure.fs_broker.routers.notifications import notification_router


broker = RabbitBroker(settings.fs.rabbit_url)
app = FastStream(broker)

broker.include_router(notification_router)

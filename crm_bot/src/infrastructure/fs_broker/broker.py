from faststream.rabbit import RabbitBroker
from faststream import FastStream
from core import settings
from pydantic import BaseModel


class TestMsg(BaseModel):
    body: str


broker = RabbitBroker(settings.fs.rabbit_url)
app = FastStream(broker)

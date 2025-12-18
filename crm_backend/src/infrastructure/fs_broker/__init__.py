from infrastructure.fs_broker.broker import broker
from infrastructure.fs_broker.router.booking_router import booking_router


broker.include_router(booking_router)

from infrastructure.fs_broker.broker import broker
from infrastructure.fs_broker.router.booking_router import booking_router
from infrastructure.fs_broker.router.tg_user_router import tg_user_router


broker.include_router(tg_user_router)
broker.include_router(booking_router)

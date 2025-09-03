__all__ = ("main_router",)

from aiogram import Router
from .start import router as start_router
from .booking import router as booking_router


def main_router() -> Router:
    router = Router()

    router.include_routers(start_router, booking_router)

    return router

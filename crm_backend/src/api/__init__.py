from fastapi import APIRouter
from core.config import settings
from api.auth.views import router as auth_router
from api.employees.views import router as employees_router
from api.users.views import router as users_router
from api.positions.views import router as positions_router
from api.categories.views import router as categories_router
from api.services.views import router as services_router
from api.booking.views import router as booking_router

api_router = APIRouter(prefix=settings.api_prefix.api_v1)
api_router.include_router(auth_router)
api_router.include_router(employees_router)
api_router.include_router(users_router)
api_router.include_router(positions_router)
api_router.include_router(categories_router)
api_router.include_router(services_router)
api_router.include_router(booking_router)

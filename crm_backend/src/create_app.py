from fastapi.responses import ORJSONResponse
from typing import AsyncGenerator
from fastapi import FastAPI
from infrastructure import db_helper
from api import api_router
from core import register_error_handlers, register_middleware


async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield
    await db_helper.dispose()


def create_app():
    app = FastAPI(
        lifespan=lifespan,
        title="srmAPI",
        default_response_class=ORJSONResponse,
    )

    register_middleware(app)
    register_error_handlers(app)

    app.include_router(api_router)

    return app

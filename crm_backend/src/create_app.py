from fastapi.responses import ORJSONResponse
from typing import AsyncGenerator
from fastapi import FastAPI
from infrastructure import db_helper
from infrastructure.fs_broker.broker import broker, fs_app
from api import api_router
from core import register_error_handlers, register_middleware
from faststream.asgi import make_asyncapi_asgi


async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:

    await broker.start()

    yield

    await db_helper.dispose()
    await broker.close()


def create_app():
    app = FastAPI(
        lifespan=lifespan,
        title="CrmAPI",
        default_response_class=ORJSONResponse,
    )

    register_middleware(app)
    register_error_handlers(app)

    app.include_router(api_router)

    # faststream docs
    app.mount("/docs/asyncapi", make_asyncapi_asgi(fs_app))

    return app

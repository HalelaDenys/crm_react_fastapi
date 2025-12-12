from faststream import Header
from core import settings, AuthError
from typing import Annotated


async def verify_tg_request(authorization: Annotated[str, Header()]):
    if authorization != f"Bearer {settings.fs.tg_api_secret}":
        raise AuthError("Not allowed")

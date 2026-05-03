import asyncio
import logging
import random
from functools import wraps
from typing import Callable, Any

from httpx import HTTPStatusError, RequestError, TimeoutException

logger = logging.getLogger(__name__)


def retry(max_attempts: int = 3, delay: float = 1) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)

                except (HTTPStatusError, RequestError, TimeoutException) as e:

                    if isinstance(e, HTTPStatusError):
                        status = e.response.status_code
                        if status not in (408, 429) and status < 500:
                            raise

                    last_exception = e

                    logger.warning(
                        "Attempt %s/%s http failed: %s",
                        attempt,
                        max_attempts,
                        e,
                    )

                except Exception as e:
                    last_exception = e
                    logger.warning(
                        "Attempt %s/%s error: %s",
                        attempt,
                        max_attempts,
                        e,
                    )

                if attempt < max_attempts:
                    sleep = delay * (2 ** (attempt - 1))
                    await asyncio.sleep(sleep + random.uniform(0, 0.3))

            raise last_exception

        return wrapper

    return decorator

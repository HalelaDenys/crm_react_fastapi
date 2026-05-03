from httpx import AsyncClient, HTTPStatusError, RequestError, Timeout, Limits
import logging
from core import retry

logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self, base_url: str, token: str | None = None):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self._client: AsyncClient | None = None

    async def connect(self) -> None:
        if self._client:
            return

        self._client = AsyncClient(
            timeout=Timeout(10.0),
            limits=Limits(
                max_connections=100,
                max_keepalive_connections=20,
            ),
        )

    async def close(self):
        if self._client:
            await self._client.aclose()
            self._client = None

    def _get_client(self) -> AsyncClient:
        if not self._client:
            raise RuntimeError("HTTP client is not initialized. Call connect() first.")
        return self._client

    @retry(max_attempts=5)
    async def get(self, path: str, params: dict | None = None) -> dict | list:
        headers = self._get_headers()
        client = self._get_client()
        response = await client.get(
            f"{self.base_url}{path}", params=params, headers=headers
        )
        response.raise_for_status()
        return response.json()

    def _get_headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

from httpx import AsyncClient, HTTPStatusError, RequestError
from typing import Any


class APIClient:
    def __init__(self, base_url: str, token: str | None = None):
        self.base_url = base_url.rstrip("/")
        self.token = token

    async def get(self, path: str, params: dict | None = None) -> Any | dict | list:
        headers = self._get_headers()
        try:
            async with AsyncClient(timeout=10) as client:
                response = await client.get(
                    f"{self.base_url}{path}", params=params, headers=headers
                )
                response.raise_for_status()
                return response.json()
        except HTTPStatusError as e:
            print(f"HTTP помилка: {e.response.status_code} - {e.response.text}")
        except RequestError as e:
            print(f"Помилка запиту: {e}")

    async def post(self, path: str, data: dict) -> Any | dict | list:
        headers = self._get_headers()
        try:
            async with AsyncClient(timeout=10) as client:
                response = await client.post(
                    f"{self.base_url}{path}", json=data, headers=headers
                )
                response.raise_for_status()
                return response.json()
        except HTTPStatusError as e:
            print(f"HTTP помилка: {e.response.status_code} - {e.response.text}")
        except RequestError as e:
            print(f"Помилка запиту: {e}")

    def _get_headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

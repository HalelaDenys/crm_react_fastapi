from core.base_client import APIClient
from core import settings


class ServiceAPI(APIClient):
    async def get_category(self) -> list[dict[str, str]]:
        categories = await self.get("/categories")
        return [
            {"text": category["name"], "call": f"category:{category['id']}"}
            for category in categories
        ]

    async def get_service_by_category(self, category_id: int) -> list[dict[str, str]]:
        services = await self.get(f"/services/categories/{category_id}")
        if not services:
            return []
        return [
            {"text": service["name"], "call": f"service:{service['id']}"}
            for service in services
        ]

    async def get_available_slots(self, service_id: int, booking_date: str) -> list:
        services = await self.get(
            f"/booking/services/{service_id}/available-slots?booking_date={booking_date}",
        )
        if not services:
            return []
        return [
            {
                "text": service["start"],
                "call": f"recording_time:{service['start'].replace(':', '-')}",
            }
            for service in services
        ]

    async def add_booking(self, booking_data: dict) -> None:
        await self.post(
            f"/booking",
            data=booking_data,
        )
        return


api = ServiceAPI(base_url=settings.api.base_url)

from schemas.service_shemas import CreateServiceSchema
from infrastructure import Service, ServiceRepository
import pytest


@pytest.mark.asyncio
class TestServiceRepo:
    async def test_create_service(
        self,
        service_repo: ServiceRepository,
        air_filter_replacement_test_data: CreateServiceSchema,
    ) -> None:
        service = await service_repo.create(data=air_filter_replacement_test_data)

        assert service is not None
        assert service.id is not None
        assert service.name == air_filter_replacement_test_data.name

    async def test_get_service(
        self,
        service_repo: ServiceRepository,
        oil_filter_replacement_test_data: CreateServiceSchema,
    ) -> None:
        service = await service_repo.find_single(id=1)

        assert service is not None
        assert service.id == 1
        assert service.name == oil_filter_replacement_test_data.name
        assert service.price == oil_filter_replacement_test_data.price

    async def test_update_service(self, service_repo: ServiceRepository) -> None:
        pass

    async def test_find_all_services(self, service_repo: ServiceRepository) -> None:
        services = await service_repo.find_all()

        assert len(services) > 0
        assert isinstance(services, list)
        assert isinstance(services[0], Service)

    async def test_find_all_pagination(self, service_repo: ServiceRepository) -> None:
        services = await service_repo.find_all_pag(category_id=1, page=1, limit=2)
        assert isinstance(services, tuple)

        assert len(services) == 2
        assert len(services[0]) <= 2

        assert isinstance(services[0], list)
        assert isinstance(services[1], bool)
        assert isinstance(services[0][0], Service)

    async def test_delete_service(self, service_repo: ServiceRepository) -> None:
        await service_repo.delete(id=1)

        service = await service_repo.find_single(id=1)
        assert service is None

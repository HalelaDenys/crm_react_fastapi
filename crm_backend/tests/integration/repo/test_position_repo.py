from schemas.position_shemas import CreatePositionSchema
from infrastructure import Position, PositionRepository
import pytest


@pytest.mark.asyncio
class TestPositionRepository:

    async def test_create_position(
        self, pos_repo: PositionRepository, position_test_data: CreatePositionSchema
    ) -> None:
        position = await pos_repo.create(data=position_test_data)

        assert position is not None
        assert position.name == position_test_data.name

    @pytest.mark.parametrize("pos_id, name", [(1, "admin"), (2, "manager")])
    async def test_get_position(
        self, pos_repo: PositionRepository, pos_id: int, name: str
    ) -> None:
        position = await pos_repo.find_single(id=pos_id)

        assert position is not None
        assert position.name == name

    async def test_update_position(self, pos_repo: PositionRepository) -> None:
        new_data = CreatePositionSchema(name="superuser")
        position = await pos_repo.update(data=new_data, id=1)

        assert position is not None
        assert position.name == new_data.name

    async def test_find_all_positions(self, pos_repo: PositionRepository) -> None:
        positions = await pos_repo.find_all()

        assert isinstance(positions, list)
        assert len(positions) > 0
        assert isinstance(positions[0], Position)

    async def test_delete_position(self, pos_repo: PositionRepository) -> None:
        await pos_repo.delete(id=2)
        position = await pos_repo.find_single(id=2)
        assert position is None

import pytest
from schemas.position_shemas import CreatePositionSchema


@pytest.fixture
def position_test_data() -> CreatePositionSchema:
    return CreatePositionSchema(
        name="mechanic",
    )


mechanic_pos = {
    "name": "mechanic",
}

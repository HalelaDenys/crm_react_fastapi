from schemas.category_schema import CreateCategorySchema
from infrastructure import Category, CategoryRepository
import pytest


@pytest.mark.asyncio
class TestCategoryRepository:
    async def test_create_category(
        self,
        category_repo: CategoryRepository,
        bodywork_test_data: CreateCategorySchema,
    ) -> None:
        category = await category_repo.create(data=bodywork_test_data)

        assert category is not None
        assert category.id is not None
        assert category.name == bodywork_test_data.name

    @pytest.mark.parametrize(
        "cat_id, name",
        [
            (1, "quick works"),
            (2, "diagnostics"),
        ],
    )
    async def test_get_category(
        self, category_repo: CategoryRepository, cat_id: int, name: str
    ) -> None:
        category = await category_repo.find_single(id=cat_id)

        assert category is not None
        assert category.id == cat_id
        assert category.name == name

    async def test_update_category(self, category_repo: CategoryRepository) -> None:
        new_data = CreateCategorySchema(name="quick diagnostics")

        category = await category_repo.update(id=1, data=new_data)
        assert category is not None
        assert category.name == new_data.name

    async def test_find_all_category(self, category_repo: CategoryRepository) -> None:
        categories = await category_repo.find_all()

        assert len(categories) > 0
        assert isinstance(categories, list)
        assert isinstance(categories[0], Category)

    async def test_delete_category(self, category_repo: CategoryRepository) -> None:
        await category_repo.delete(id=1)

        category = await category_repo.find_single(id=1)
        assert category is None

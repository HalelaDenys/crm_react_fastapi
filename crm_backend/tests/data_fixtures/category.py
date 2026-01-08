from schemas.category_schema import CreateCategorySchema
import pytest


@pytest.fixture
def quick_works_test_data() -> CreateCategorySchema:
    return CreateCategorySchema(
        name="quick works",
    )


@pytest.fixture
def diagnostics_test_data() -> CreateCategorySchema:
    return CreateCategorySchema(
        name="diagnostics",
    )


@pytest.fixture
def bodywork_test_data() -> CreateCategorySchema:
    return CreateCategorySchema(
        name="bodywork",
    )


quick_works = {
    "name": "quick works",
}

diagnostics = {
    "name": "diagnostics",
}
bodywork = {
    "name": "bodywork",
}

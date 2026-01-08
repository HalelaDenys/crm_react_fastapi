from schemas.service_shemas import CreateServiceSchema
import pytest


@pytest.fixture
def oil_filter_replacement_test_data() -> CreateServiceSchema:
    return CreateServiceSchema(
        name=oil_filter_replacement["name"],
        duration_minutes=oil_filter_replacement["duration_minutes"],
        price=oil_filter_replacement["price"],
        category_id=oil_filter_replacement["category_id"],
    )


@pytest.fixture
def air_filter_replacement_test_data() -> CreateServiceSchema:
    return CreateServiceSchema(
        name=air_filter_replacement["name"],
        duration_minutes=air_filter_replacement["duration_minutes"],
        price=air_filter_replacement["price"],
        category_id=air_filter_replacement["category_id"],
    )


@pytest.fixture
def brake_diagnostics_test_data() -> CreateServiceSchema:
    return CreateServiceSchema(
        name=brake_diagnostics["name"],
        duration_minutes=brake_diagnostics["duration_minutes"],
        price=brake_diagnostics["price"],
        category_id=brake_diagnostics["category_id"],
    )


@pytest.fixture
def engine_diagnostics_test_data() -> CreateServiceSchema:
    return CreateServiceSchema(
        name=engine_diagnostics["name"],
        duration_minutes=engine_diagnostics["duration_minutes"],
        price=engine_diagnostics["price"],
        category_id=engine_diagnostics["category_id"],
    )


oil_filter_replacement = {
    "name": "Oil filter replacement",
    "duration_minutes": 45,
    "price": 25,
    "category_id": 1,
}

air_filter_replacement = {
    "name": "Air filter replacement",
    "duration_minutes": 45,
    "price": 15,
    "category_id": 1,
}

brake_diagnostics = {
    "name": "Brake diagnostics",
    "duration_minutes": 45,
    "price": 30,
    "category_id": 2,
}

engine_diagnostics = {
    "name": "Engine diagnostics",
    "duration_minutes": 45,
    "price": 55,
    "category_id": 2,
}

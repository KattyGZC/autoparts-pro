import pytest
from app.main import app
from app.adapters.routers.repair_order_router import get_db
from tests.test_db import override_get_db, init_test_db

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    init_test_db()
    app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def db():
    yield from override_get_db()
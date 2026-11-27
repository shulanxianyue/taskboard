import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers import tasks


@pytest.fixture(autouse=True)
def clean_storage():
    tasks.reset_storage()
    yield
    tasks.reset_storage()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)

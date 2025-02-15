import asyncio

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient

from report.routers import report_endpoints


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
async def mock_mongodb(monkeypatch):
    """Create mock MongoDB client and patch it at module level."""
    # Create async client for the endpoints
    async_client = AsyncMongoMockClient()
    async_db = async_client["faculty-reports"]
    async_collection = async_db["teachers_reports"]

    # Patch at the module level where the database is imported
    monkeypatch.setattr("report.models.database.client", async_client)
    monkeypatch.setattr("report.models.database.database", async_db)
    monkeypatch.setattr(
        "report.models.database.teachers_reports_collection", async_collection
    )
    monkeypatch.setattr(
        "report.routers.report_endpoints.teachers_reports_collection", async_collection
    )

    yield async_collection

    # Clean up after test
    await async_collection.delete_many({})


@pytest.fixture
def app():
    """Create a FastAPI app for testing."""
    app = FastAPI()
    app.include_router(report_endpoints.router, prefix="/report")
    return app


@pytest.fixture
def client(app):
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def sample_teacher_report():
    """Create a sample teacher report for testing."""
    return {
        "teacher": "John Doe",
        "subject": "Advanced Programming",
        "hours_lectures": 30,
        "hours_exercises": 30,
        "study_year": 2,
        "semester": 1,
    }

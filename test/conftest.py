import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app
from app.models import Base
from app.database import get_db


def pytest_configure(config):
    config.option.asyncio_default_fixture_loop_scope = 'function'


engine = create_engine(
    "sqlite:///:memory:?check_same_thread=False",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    db_session = TestingSessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


@pytest.fixture
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    return TestClient(app)


@pytest.fixture
def auth_headers():
    return {"x-api-key": "omidghamiloo"}

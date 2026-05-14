import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from alembic import command
from alembic.config import Config

import app.model  # ensure Task and Category are registered on Base.metadata

from app.main import app
from app.database import get_db


TEST_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg2://tasks:tasks@localhost:5433/tasks_test",
)

engine = create_engine(TEST_URL)
TestingSession = sessionmaker(bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    cfg = Config("alembic.ini")
    cfg.set_main_option("sqlalchemy.url", TEST_URL)
    command.upgrade(cfg, "head")
    yield
    # No teardown — tmpfs container dies and takes the data with it.

@pytest.fixture(autouse=True)
def clean_tables():
    yield
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE tasks, categories RESTART IDENTITY CASCADE"))

@pytest.fixture
def client():
    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()       
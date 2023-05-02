# pylint: disable= missing-module-docstring, missing-function-docstring
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import tests.util.constants as c
from tests.util.assert_helpers import are_equal

from trainings.main import app, get_db, BASE_URI
from trainings.database.models import Base
from trainings.database.data import init_db

# Setup

client = TestClient(app)

SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
init_db(TestingSessionLocal())


def override_get_db():
    database = TestingSessionLocal()
    try:
        yield database
    finally:
        database.close()


app.dependency_overrides[get_db] = override_get_db


def test_get_all_trainings():
    response = client.get(BASE_URI)
    assert response.status_code == 200
    assert are_equal(response.json(), c.EXPECTED_TRAININGS, {})


def test_get_all_trainings_with_pagination():
    expected_pagination = {"offset": 10, "limit": 30}
    response = client.get(BASE_URI, params=expected_pagination)
    assert response.status_code == 200
    assert response.json()["offset"] == 10
    assert response.json()["limit"] == 30

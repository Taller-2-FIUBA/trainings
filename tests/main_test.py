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
    expected_trainings = [c.FIRST_TRAINING, c.TOMATO_TRAINING]
    response = client.get(BASE_URI)
    assert response.status_code == 200
    assert are_equal(
        response.json(),
        c.EMPTY_RESPONSE_WITH_PAGINATION | {"items": expected_trainings},
        {}
    )


def test_get_all_trainings_with_pagination():
    expected_pagination = {"offset": 10, "limit": 30}
    response = client.get(BASE_URI, params=expected_pagination)
    assert response.status_code == 200
    assert response.json()["offset"] == 10
    assert response.json()["limit"] == 30


def test_when_filtering_by_trainer_id_tomate_returns_tomato_training():
    response = client.get(BASE_URI, params={"trainer_id": "tomato"})
    assert response.status_code == 200
    assert are_equal(
        response.json(),
        c.EMPTY_RESPONSE_WITH_PAGINATION | {"items": [c.TOMATO_TRAINING]},
        {},
    )


def test_when_filtering_by_type_cardio_returns_first_training():
    response = client.get(BASE_URI, params={"training_type": "Cardio"})
    assert response.status_code == 200
    assert are_equal(
        response.json(),
        c.EMPTY_RESPONSE_WITH_PAGINATION | {"items": [c.FIRST_TRAINING]},
        {},
    )


def test_when_filtering_by_difficulty_easy_returns_tomato_training():
    response = client.get(BASE_URI, params={"difficulty": "Medium"})
    assert response.status_code == 200
    assert are_equal(
        response.json(),
        c.EMPTY_RESPONSE_WITH_PAGINATION | {"items": [c.TOMATO_TRAINING]},
        {},
    )


def test_when_filtering_by_all_available_fields_expect_first_training():
    filters = {
        "trainer_id": "Ju6JXm1S8rVQfyC18mqL418JdgE2",
        "training_type": "Cardio",
        "difficulty": "Easy",
        "offset": 0,
        "limit": 1,
    }
    response = client.get(BASE_URI, params=filters)
    assert response.status_code == 200
    expected_response = {
        "items": [c.FIRST_TRAINING],
        "offset": 0,
        "limit": 1,
    }
    assert are_equal(response.json(), expected_response, {})


def test_when_filtering_by_trainer_id_banana_returns_no_training():
    response = client.get(BASE_URI, params={"trainer_id": "banana"})
    assert response.status_code == 200
    assert are_equal(response.json(), c.EMPTY_RESPONSE_WITH_PAGINATION, {})


def test_post_training():
    response = client.post(BASE_URI, json=c.TRAINING_TO_BE_CREATED)
    assert response.status_code == 200
    assert are_equal(
        response.json(),
        c.TRAINING_TO_BE_CREATED | {"rating": 0},
        {"id"}
    )


def test_get_training_by_id():
    response = client.get(BASE_URI + "/1")
    assert response.status_code == 200
    assert are_equal(response.json(), c.FIRST_TRAINING, {})

# pylint: disable= missing-module-docstring, missing-function-docstring
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import tests.util.constants as c
from tests.util.assert_helpers import are_equal

from trainings.main import EXERCISES_URI, TYPES_URI, app, get_db, BASE_URI
from trainings.database.models import Base
from trainings.database.data import init_db

GET_PERMISSIONS_MOCK = MagicMock(return_value={"a": "b"})
FIREBASE_SAVE_MOCK = MagicMock(return_value="a_firebase_id")

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


@patch("trainings.main.get_permissions", GET_PERMISSIONS_MOCK)
@patch("trainings.main.assert_can_create_training")
@patch("trainings.main.save", FIREBASE_SAVE_MOCK)
def test_post_training(assert_can_create_training_mock):
    response = client.post(BASE_URI, json=c.TRAINING_TO_BE_CREATED)
    assert response.status_code == 200
    values_to_override = {
        "rating": 0,
        "media": "a_firebase_id",
        "blocked": False,
    }
    assert are_equal(
        response.json(),
        c.TRAINING_TO_BE_CREATED | values_to_override,
        {"id"}
    )
    GET_PERMISSIONS_MOCK.assert_called_once()
    assert_can_create_training_mock.assert_called_once_with({"a": "b"})
    FIREBASE_SAVE_MOCK.assert_called_once_with("blobOfMedia")


def test_get_training_by_id():
    response = client.get(BASE_URI + "/1")
    assert response.status_code == 200
    assert are_equal(response.json(), c.FIRST_TRAINING, {})


def test_when_getting_training_types_expect_list():
    response = client.get(TYPES_URI)
    assert response.status_code == 200, response.json()
    assert are_equal(response.json(), c.EXPECTED_TRAINING_TYPES, {})


def test_when_getting_exercises_expect_list():
    response = client.get(EXERCISES_URI)
    assert response.status_code == 200, response.json()
    assert are_equal(response.json(), c.EXPECTED_EXERCISES, {})

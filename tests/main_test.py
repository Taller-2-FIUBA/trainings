# pylint: disable= missing-module-docstring, missing-function-docstring
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import tests.util.constants as c
from tests.util.assert_helpers import are_equal
from tests.util.data import init_test_db

from trainings.main import EXERCISES_URI, TYPES_URI, app, get_db, BASE_URI
from trainings.database.models import Base

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
init_test_db(TestingSessionLocal())


def override_get_db():
    database = TestingSessionLocal()
    try:
        yield database
    finally:
        database.close()


app.dependency_overrides[get_db] = override_get_db


def test_get_all_trainings():
    expected_trainings = [
        c.FIRST_TRAINING,
        c.TOMATO_TRAINING,
        c.TO_BLOCK_TRAINING,
    ]
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


def test_when_filtering_training_by_type_finger_expect_error():
    response = client.get(BASE_URI, params={"training_type": "finger"})
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Could not save training. Type finger not found."
    }


def test_when_filtering_by_difficulty_easy_returns_tomato_training():
    response = client.get(BASE_URI, params={"difficulty": "Medium"})
    assert response.status_code == 200
    assert are_equal(
        response.json(),
        c.EMPTY_RESPONSE_WITH_PAGINATION | {"items": [c.TOMATO_TRAINING]},
        {},
    )


def test_when_filtering_training_by_difficulty_beginner_expect_error():
    response = client.get(BASE_URI, params={"difficulty": "beginner"})
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Could not save training. Difficulty beginner not found."
    }


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


def test_when_creating_training_without_tittle_expect_error():
    response = client.post(
        BASE_URI, json=c.TRAINING_TO_BE_CREATED | {"tittle": None}
    )
    assert response.status_code == 422
    expected_error = {
        "detail": [
            {
                "loc": [
                    "body",
                    "tittle"
                ],
                "msg": "none is not an allowed value",
                "type": "type_error.none.not_allowed"
            }
        ]
    }
    assert response.json() == expected_error


def test_when_creating_training_without_description_expect_error():
    response = client.post(
        BASE_URI, json=c.TRAINING_TO_BE_CREATED | {"description": None}
    )
    assert response.status_code == 422
    expected_error = {
        "detail": [
            {
                "loc": [
                    "body",
                    "description"
                ],
                "msg": "none is not an allowed value",
                "type": "type_error.none.not_allowed"
            }
        ]
    }
    assert response.json() == expected_error


def test_when_creating_training_without_trainer_id_expect_error():
    response = client.post(
        BASE_URI, json=c.TRAINING_TO_BE_CREATED | {"trainer_id": None}
    )
    assert response.status_code == 422
    expected_error = {
        "detail": [
            {
                "loc": [
                    "body",
                    "trainer_id"
                ],
                "msg": "none is not an allowed value",
                "type": "type_error.none.not_allowed"
            }
        ]
    }
    assert response.json() == expected_error


def test_when_creating_training_without_difficulty_expect_error():
    response = client.post(
        BASE_URI, json=c.TRAINING_TO_BE_CREATED | {"difficulty": None}
    )
    assert response.status_code == 422
    expected_error = {
        "detail": [
            {
                "loc": [
                    "body",
                    "difficulty"
                ],
                "msg": "none is not an allowed value",
                "type": "type_error.none.not_allowed"
            }
        ]
    }
    assert response.json() == expected_error


def test_when_creating_training_without_type_expect_error():
    response = client.post(
        BASE_URI, json=c.TRAINING_TO_BE_CREATED | {"type": None}
    )
    assert response.status_code == 422
    expected_error = {
        "detail": [
            {
                "loc": [
                    "body",
                    "type"
                ],
                "msg": "none is not an allowed value",
                "type": "type_error.none.not_allowed"
            }
        ]
    }
    assert response.json() == expected_error


def test_get_training_by_id():
    response = client.get(BASE_URI + "/1")
    assert response.status_code == 201
    assert are_equal(response.json(), c.FIRST_TRAINING, {})


def test_when_getting_training_of_id_999_expect_error():
    response = client.get(BASE_URI + "/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Training not found."}


def test_when_getting_training_types_expect_list():
    response = client.get(TYPES_URI)
    assert response.status_code == 200, response.json()
    assert are_equal(response.json(), c.EXPECTED_TRAINING_TYPES, {})


def test_when_getting_exercises_expect_list():
    response = client.get(EXERCISES_URI)
    assert response.status_code == 200, response.json()
    assert are_equal(response.json(), c.EXPECTED_EXERCISES, {})


def test_when_blocking_training_of_id_3_expect_blocked_to_be_true():
    url = BASE_URI + "/3"
    ignored_values = {"rating", "media"}
    unblocked_training = c.TO_BLOCK_TRAINING | {"blocked": False}
    blocked_training = c.TO_BLOCK_TRAINING | {"blocked": True}
    # Assert that is not blocked when starting
    response = client.get(url)
    assert response.status_code == 201
    assert are_equal(response.json(), unblocked_training, ignored_values)
    # Block it
    response = client.patch(url, json={"blocked": True})
    assert response.status_code == 204, response.json()
    # Assert it is blocked
    response = client.get(url)
    assert response.status_code == 201
    assert are_equal(response.json(), blocked_training, ignored_values)
    # Unblock it
    response = client.patch(url, json={"blocked": False})
    assert response.status_code == 204, response.json()
    # Assert it is unblocked
    response = client.get(url)
    assert response.status_code == 201
    assert are_equal(response.json(), unblocked_training, ignored_values)


def test_when_blocking_training_of_id_9999_expect_error():
    response = client.patch(
        BASE_URI + "/999", json={"blocked": True}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Training not found."}


def test_when_add_a_training_for_a_user_expect_204():
    response = client.post("/users/1/trainings", json={"training_id": 1})
    assert response.status_code == 204, response.json()


def test_when_add_not_existing_training_for_a_user_expect_404():
    response = client.post("/users/1/trainings", json={"training_id": 999})
    assert response.status_code == 404, response.json()
    assert response.json() == {"detail": "Training not found."}


def test_when_add_training_for_not_existing_user_expect_404():
    response = client.post("/users/999/trainings", json={"training_id": 1})
    assert response.status_code == 404, response.json()
    assert response.json() == {"detail": "User not found."}


def test_when_getting_trainings_for_a_user_expect_first_and_tomato():
    response = client.get("/users/2/trainings")
    assert response.status_code == 200, response.json()
    expected_trainings = [c.FIRST_TRAINING, c.TOMATO_TRAINING]
    assert are_equal(
        response.json(),
        c.EMPTY_RESPONSE_WITH_PAGINATION | {"items": expected_trainings},
        {},
    )


def test_when_getting_trainings_for_a_user_without_favourites_expect_empty():
    response = client.get("/users/3/trainings")
    assert response.status_code == 200, response.json()
    assert are_equal(response.json(), c.EMPTY_RESPONSE_WITH_PAGINATION, {})


def test_when_getting_trainings_for_not_existing_user_expect_404():
    response = client.post("/users/999/trainings", json={"training_id": 1})
    assert response.status_code == 404, response.json()
    assert response.json() == {"detail": "User not found."}


HEADERS = {
    "authority": "users-ingress-taller2-marianocinalli.cloud.okteto.net",
    "accept": "/",
    "accept-language": "en-US,en;q=0.9,es;q=0.8,pt;q=0.7,la;q=0.6",
    "access-control-request-headers": "authorization",
    "access-control-request-method": "patch",
    "cache-control": "no-cache",
    "origin": "https://fiufit-backoffice-6kwbytb6g-fiufitgrupo5-gmailcom"
    ".vercel.app",
    "pragma": "no-cache",
    "referer": "http://localhost:3000/",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    "(KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
}


def test_when_asking_cors_is_available_for_patch_expect_200():
    response = client.options(BASE_URI, headers=HEADERS)
    assert response.status_code == 200


def test_when_asking_cors_is_available_for_patch_uppercase_expect_200():
    method_override = {"access-control-request-method": "PATCH"}
    response = client.options(BASE_URI, headers=HEADERS | method_override)
    assert response.status_code == 200


def test_when_asking_cors_is_available_for_post_expect_200():
    method_override = {"access-control-request-method": "post"}
    response = client.options(BASE_URI, headers=HEADERS | method_override)
    assert response.status_code == 200


def test_when_asking_cors_is_available_for_post_uppercase_expect_200():
    method_override = {"access-control-request-method": "POST"}
    response = client.options(BASE_URI, headers=HEADERS | method_override)
    assert response.status_code == 200


def test_when_asking_cors_is_available_for_banana_expect_400():
    method_override = {"access-control-request-method": "banana"}
    response = client.options(BASE_URI, headers=HEADERS | method_override)
    assert response.status_code == 400


def test_when_asking_cors_is_available_origin_localhost_expect_200():
    method_override = {"origin": "localhost"}
    response = client.options(BASE_URI, headers=HEADERS | method_override)
    assert response.status_code == 200


def test_when_asking_cors_is_available_origin_localhost_3000_expect_200():
    method_override = {"origin": "localhost:3000"}
    response = client.options(BASE_URI, headers=HEADERS | method_override)
    assert response.status_code == 200


def test_when_asking_cors_is_available_origin_http_localhost_expect_200():
    method_override = {"origin": "http://localhost"}
    response = client.options(BASE_URI, headers=HEADERS | method_override)
    assert response.status_code == 200


def test_when_asking_cors_is_available_origin_https_localhost_expect_200():
    method_override = {"origin": "https://localhost"}
    response = client.options(BASE_URI, headers=HEADERS | method_override)
    assert response.status_code == 200


def test_when_asking_cors_is_available_origin_http_localhost_3000_expect_200():
    method_override = {"origin": "http://localhost"}
    response = client.options(BASE_URI, headers=HEADERS | method_override)
    assert response.status_code == 200


def test_when_asking_cors_is_available_origin_https_localhost_3000_expect_ok():
    method_override = {"origin": "https://localhost"}
    response = client.options(BASE_URI, headers=HEADERS | method_override)
    assert response.status_code == 200


def test_when_asking_cors_is_available_origin_local_expect_200():
    method_override = {"origin": "local"}
    response = client.options(BASE_URI, headers=HEADERS | method_override)
    assert response.status_code == 200


def test_when_asking_cors_is_available_origin_local_3000_expect_200():
    method_override = {"origin": "local:3000"}
    response = client.options(BASE_URI, headers=HEADERS | method_override)
    assert response.status_code == 200


def test_when_asking_cors_is_available_origin_vercel_dev_expect_200():
    method_override = {"origin": "https://fiufit-backoffice.vercel.app/"}
    response = client.options(BASE_URI, headers=HEADERS | method_override)
    assert response.status_code == 200


def test_when_asking_cors_is_available_origin_apple_expect_200():
    method_override = {"origin": "apple"}
    response = client.options(BASE_URI, headers=HEADERS | method_override)
    assert response.status_code == 400

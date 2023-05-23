# pylint: disable= missing-module-docstring, missing-function-docstring

from unittest.mock import MagicMock, patch
from trainings.trainings.hydrator import hydrate


@patch("trainings.trainings.hydrator.read", return_value="blob")
def test_when_hydrating_training_with_media_expect_read_call(
    save_spy: MagicMock,
):
    config_dummy = MagicMock()
    training_stub = MagicMock(**{
        "media": "firebase_file_name",
        "id": 1,
        "trainer_id": 1,
        "title": "A",
        "description": "B",
        "difficulty.name": "C",
        "type.name": "D",
        "blocked": True,
        "exercises": [],
    })
    training_out = hydrate(training_stub, config_dummy)
    assert training_out.media == "blob"
    assert training_out.id == 1
    assert training_out.trainer_id == "1"
    assert training_out.title == "A"
    assert training_out.description == "B"
    assert training_out.difficulty == "C"
    assert training_out.type == "D"
    assert training_out.rating == 0
    assert training_out.blocked
    assert training_out.exercises == []
    save_spy.assert_called_once_with("firebase_file_name", config_dummy)


@patch("trainings.trainings.hydrator.read", return_value="blob")
def test_when_hydrating_training_without_media_expect_no_read_call(
    save_spy: MagicMock,
):
    config_dummy = MagicMock()
    training_stub = MagicMock(**{
        "media": None,
        "id": 1,
        "trainer_id": 1,
        "title": "A",
        "description": "B",
        "difficulty.name": "C",
        "type.name": "D",
        "blocked": True,
        "exercises": [],
    })
    training_out = hydrate(training_stub, config_dummy)
    assert training_out.media is None
    assert training_out.id == 1
    assert training_out.trainer_id == "1"
    assert training_out.title == "A"
    assert training_out.description == "B"
    assert training_out.difficulty == "C"
    assert training_out.type == "D"
    assert training_out.rating == 0
    assert training_out.blocked
    assert training_out.exercises == []
    save_spy.assert_not_called()

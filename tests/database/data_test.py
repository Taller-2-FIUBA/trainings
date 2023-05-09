# pylint: disable= missing-module-docstring, missing-function-docstring
from unittest.mock import ANY, MagicMock, patch
from trainings.database.data import (
    get_training_difficulties,
    get_training_types,
    get_exercises,
    get_columns_and_cells,
    init_db,
    insert_in_postgres_ignoring_existing,
    insert_training_types,
)
from trainings.database.models import TrainingType


def test_when_getting_training_types_for_insert_expect_values():
    assert get_columns_and_cells(get_training_types()) == [
        {"id": 1, "name": "Cardio"},
        {"id": 2, "name": "Leg"},
        {"id": 3, "name": "Arm"},
        {"id": 4, "name": "Chest"},
        {"id": 5, "name": "Back"},
        {"id": 6, "name": "Abdomen"},
    ]


def test_when_getting_training_difficulties_for_insert_expect_values():
    assert get_columns_and_cells(get_training_difficulties()) == [
        {"id": 1, "name": "Easy"},
        {"id": 2, "name": "Medium"},
        {"id": 3, "name": "Hard"},
    ]


def test_when_getting_training_exercises_for_insert_expect_values():
    assert get_columns_and_cells(get_exercises()) == [
        {"id": 1, "name": "Walk", "type_id": 1, "unit": "metre"},
        {"id": 2, "name": "Walk", "type_id": 1, "unit": "second"},
        {"id": 3, "name": "Run", "type_id": 1, "unit": "metre"},
        {"id": 4, "name": "Run", "type_id": 1, "unit": "second"},
        {"id": 5, "name": "Jumping jacks", "type_id": 1, "unit": None},
        {"id": 20, "name": "Squat", "type_id": 2, "unit": None},
        {"id": 21, "name": "Lunge", "type_id": 2, "unit": None},
        {"id": 22, "name": "Deadlift", "type_id": 2, "unit": None},
        {"id": 30, "name": "Bicep curl", "type_id": 3, "unit": None},
        {"id": 31, "name": "Hammer curl", "type_id": 3, "unit": None},
        {"id": 40, "name": "Tricep dips", "type_id": 3, "unit": None},
        {"id": 41, "name": "Close grip push up", "type_id": 3, "unit": None},
        {"id": 42, "name": "Push-down", "type_id": 3, "unit": None},
        {"id": 50, "name": "Lateral raise", "type_id": 3, "unit": None},
        {"id": 51, "name": "Front raise", "type_id": 3, "unit": None},
        {"id": 52, "name": "Arnold press", "type_id": 3, "unit": None},
        {"id": 60, "name": "Push up", "type_id": 4, "unit": None},
        {"id": 61, "name": "Bench press", "type_id": 4, "unit": None},
        {"id": 62, "name": "Fly", "type_id": 4, "unit": None},
        {"id": 70, "name": "Pull-down", "type_id": 5, "unit": None},
        {"id": 71, "name": "Pull-up", "type_id": 5, "unit": None},
        {"id": 72, "name": "Bent-over row", "type_id": 5, "unit": None},
        {"id": 80, "name": "Crunch", "type_id": 6, "unit": None},
        {"id": 81, "name": "Bicycle crunch", "type_id": 6, "unit": None},
        {"id": 82, "name": "Plank", "type_id": 6, "unit": None},
    ]


@patch("trainings.database.data.insert")
def test_when_insert_in_postgres_ignoring_existing_expect_call(
    insert_mock: MagicMock,
):
    spy = MagicMock()
    spy.execute = MagicMock()
    dummy_table = MagicMock()
    insert_in_postgres_ignoring_existing(spy, dummy_table, MagicMock())
    insert_mock.assert_called_once_with(dummy_table)
    spy.execute.assert_called_once()


@patch("trainings.database.data.insert_in_postgres_ignoring_existing")
@patch("trainings.database.data.insert_training_types", MagicMock())
def test_when_insert_training_types_expect_call(
    insert_in_postgres_spy: MagicMock,
):
    dummy = MagicMock()
    insert_training_types(dummy)
    insert_in_postgres_spy.assert_called_once_with(dummy, TrainingType, ANY)


@patch("trainings.database.data.insert_training_types")
@patch("trainings.database.data.insert_training_difficulties")
@patch("trainings.database.data.insert_exercises")
def test_when_init_db_expect_call(
    insert_types_spy: MagicMock,
    insert_difficulties_spy: MagicMock,
    insert_exercises_spy: MagicMock,
) -> None:
    open_session_dummy = MagicMock()
    stub = MagicMock()
    stub.__enter__ = MagicMock(return_value=open_session_dummy)
    init_db(stub)
    insert_types_spy.assert_called_once_with(open_session_dummy)
    insert_difficulties_spy.assert_called_once_with(open_session_dummy)
    insert_exercises_spy.assert_called_once_with(open_session_dummy)

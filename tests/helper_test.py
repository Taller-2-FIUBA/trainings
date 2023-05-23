# pylint: disable= missing-module-docstring, missing-function-docstring
from trainings.trainings.dto import TrainingPatch
from trainings.trainings.helper import get_columns_and_values


def test_when_patch_has_all_none_expect_empty_dictionary():
    assert get_columns_and_values(TrainingPatch()) == {}


def test_when_patch_has_title_expect_title_in_dictionary():
    columns = get_columns_and_values(TrainingPatch(title="training"))
    assert columns == {"title": "training"}


def test_when_patch_has_description_expect_description_in_dictionary():
    columns = get_columns_and_values(TrainingPatch(description="description"))
    assert columns == {"description": "description"}


def test_when_patch_has_difficulty_expect_difficulty_in_dictionary():
    columns = get_columns_and_values(TrainingPatch(difficulty="Easy"))
    assert columns == {"difficulty": "Easy"}


def test_when_patch_has_media_expect_title_in_dictionary():
    columns = get_columns_and_values(TrainingPatch(media="123t24gt4g4"))
    assert columns == {"media": "123t24gt4g4"}


def test_when_patch_has_blocked_expect_blocked_in_dictionary():
    columns = get_columns_and_values(TrainingPatch(blocked=False))
    assert columns == {"blocked": False}

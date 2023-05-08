# pylint: disable= missing-module-docstring, missing-function-docstring
from fastapi import HTTPException
from pytest import raises

from trainings.authorization import assert_can_create_training


def test_when_admin_creates_training_expect_error():
    with raises(HTTPException):
        assert_can_create_training({"role": "admin"})


def test_when_athlete_creates_training_expect_error():
    with raises(HTTPException):
        assert_can_create_training({"role": "athlete"})


# To be replaced with trainer
def test_when_user_creates_training_expect_true():
    assert assert_can_create_training({"role": "user"})

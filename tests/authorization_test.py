# pylint: disable= missing-module-docstring, missing-function-docstring
from unittest.mock import MagicMock
from fastapi import HTTPException
from pytest import raises

from trainings.authorization import (
    assert_can_create_training, get_permissions
)


def test_when_external_auth_service_returns_credentials_expect_them():
    # Setup data and expectations
    expected_host = "auth-service.fiufit.svc.cluster.local:8002"
    expected_url = f"http://{expected_host}/auth/credentials"
    expected_credentials = {"role": "admin"}
    response = MagicMock()
    response.status_code = 200
    response.json = MagicMock(return_value={"data": expected_credentials})
    # Setup testing doubles
    headers_stub = MagicMock()
    headers_stub.get = MagicMock(return_value="banana")
    config_stub = MagicMock()
    config_stub.auth.host = expected_host
    client_spy = MagicMock()
    client_spy.get = MagicMock(return_value=response)
    # Exercise
    permissions = get_permissions(headers_stub, client_spy, config_stub)
    # Assert data
    assert permissions == expected_credentials
    # Assert expectations
    headers_stub.get.assert_called_once_with("Authorization")
    client_spy.get.assert_called_once_with(
        expected_url, headers={"Authorization": "banana"}
    )


def test_when_authorization_header_is_empty_expect_error():
    # Setup testing doubles
    headers = MagicMock(**{"get.return_value": None})
    # Exercise
    with raises(HTTPException):
        get_permissions(headers, MagicMock(), MagicMock())


def test_when_external_auth_service_returns_code_403_expect_error():
    response = MagicMock()
    response.status_code = 403
    client_spy = MagicMock()
    client_spy.get = MagicMock(return_value=response)
    # Exercise
    with raises(HTTPException):
        get_permissions(MagicMock(), client_spy, MagicMock())


def test_when_response_raises_expect_error():
    response = MagicMock()
    response.status_code = 200
    response.json = MagicMock(side_effect=Exception("Boom!"))
    client_spy = MagicMock()
    client_spy.get = MagicMock(return_value=response)
    # Exercise
    with raises(HTTPException):
        get_permissions(MagicMock(), client_spy, MagicMock())


def test_when_admin_creates_training_expect_error():
    with raises(HTTPException):
        assert_can_create_training({"role": "admin"})


def test_when_athlete_creates_training_expect_error():
    with raises(HTTPException):
        assert_can_create_training({"role": "athlete"})


# To be replaced with trainer
def test_when_user_creates_training_expect_true():
    assert assert_can_create_training({"role": "user"})

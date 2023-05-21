# pylint: disable= missing-module-docstring, missing-function-docstring
from unittest.mock import MagicMock, patch

from hamcrest import assert_that, matches_regexp
from trainings.firebase import get_certificate, get_file_name, save


@patch("trainings.firebase.initialize_app")
@patch("trainings.firebase.storage.bucket")
@patch("trainings.firebase.Certificate")
@patch("trainings.firebase.get_file_name", return_value="filename")
def test_saving_blob_expect_a_firebase_id(
    initialize_app_spy: MagicMock,
    storage_bucket_spy: MagicMock,
    certificate_spy: MagicMock,
    get_file_name_stub: MagicMock,
):
    # Setup data and expectations
    expected_media = "expected_media"
    expected_firebase_config = {
        "type": "service_account",
        "project_id": "taller2-fiufit",
        "private_key_id": "404e45eb1856c2152c53e2a805e59b0b186ab956",
        "private_key": "a private key",
        "storageBucket": "a bucket",
    }
    # Setup testing doubles
    config_stub = MagicMock()
    config_stub.firebase = MagicMock(
        return_value=MagicMock(expected_firebase_config)
    )
    # Exercise
    file = save(expected_media, "trainer_id", config_stub)
    # Assert data
    assert file == "filename"
    # Assert expectations
    certificate_spy.assert_called_once()
    initialize_app_spy.assert_called_once()
    get_file_name_stub.assert_called_once()
    storage_bucket_spy.assert_called_once()


def test_that_file_name_is_random():
    first = get_file_name("some_trainer_id")
    assert_that(first, matches_regexp("some_trainer_id-([A-z0-9]{32})"))
    assert first != get_file_name("some_trainer_id")
    assert first != get_file_name("some_trainer_id")


def test_when_getting_certificate_data_is_from_config():
    certificate_data = {
        "firebase.type": "type",
        "firebase.project_id": "project_id",
        "firebase.private_key_id": "private_key_id",
        "firebase.private_key": "private_key",
        "firebase.client_email": "client_email",
        "firebase.client_id": "client_id",
        "firebase.auth_uri": "auth_uri",
        "firebase.token_uri": "token_uri",
        "firebase.auth_provider_x509_cert_url": "auth_provider_x509_cert_url",
        "firebase.client_x509_cert_url": "client_x509_cert_url",
    }
    config = MagicMock(**certificate_data)
    certificate = get_certificate(config)
    assert certificate == {
        "type": "type",
        "project_id": "project_id",
        "private_key_id": "private_key_id",
        "private_key": "private_key",
        "client_email": "client_email",
        "client_id": "client_id",
        "auth_uri": "auth_uri",
        "token_uri": "token_uri",
        "auth_provider_x509_cert_url": "auth_provider_x509_cert_url",
        "client_x509_cert_url": "client_x509_cert_url",
    }

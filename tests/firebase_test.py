# pylint: disable=missing-module-docstring, missing-function-docstring
# pylint: disable=too-many-arguments
from unittest.mock import MagicMock, patch, sentinel

from hamcrest import assert_that, matches_regexp
from google.cloud.exceptions import NotFound

from trainings.firebase import (
    get_certificate,
    get_file_name,
    initialize,
    read,
    save,
)


@patch("trainings.firebase.initialize_app")
@patch("trainings.firebase.get_certificate", return_value=sentinel)
@patch("trainings.firebase.Certificate", return_value=sentinel)
@patch("trainings.firebase.get_app", side_effect=ValueError)
def test_when_firebase_is_not_initialized_expect_call_to_initialized(
    get_app_spy: MagicMock,
    certificate_spy: MagicMock,
    get_certificate_spy: MagicMock,
    initialize_app_spy: MagicMock,
):
    # Setup data
    expected_firebase_config = {
        "firebase.storage_bucket": "a bucket",
    }
    # Setup testing doubles
    config_stub = MagicMock(**expected_firebase_config)
    # Exercise
    initialize(config_stub)
    # Assert expectations
    get_app_spy.assert_called_once()
    get_certificate_spy.assert_called_once_with(config_stub)
    certificate_spy.assert_called_once_with(sentinel)
    initialize_app_spy.assert_called_once_with(
        sentinel, {"storageBucket": "a bucket"}
    )


@patch("trainings.firebase.initialize_app")
@patch("trainings.firebase.get_certificate")
@patch("trainings.firebase.Certificate")
@patch("trainings.firebase.get_app", return_value=sentinel)
def test_when_firebase_is_initialized_expect_no_call_to_initialized(
    get_app_spy: MagicMock,
    certificate_spy: MagicMock,
    get_certificate_spy: MagicMock,
    initialize_app_spy: MagicMock,
):
    # Exercise
    initialize(MagicMock())
    # Assert expectations
    get_app_spy.assert_called_once()
    get_certificate_spy.assert_not_called()
    certificate_spy.assert_not_called()
    initialize_app_spy.assert_not_called()


@patch("trainings.firebase.initialize")
@patch("trainings.firebase.storage.bucket")
@patch("trainings.firebase.get_file_name", return_value="filename")
def test_when_saving_blob_expect_filename(
    get_file_name_stub: MagicMock,
    storage_bucket_spy: MagicMock,
    initialize_spy: MagicMock,
):
    # Exercise
    file = save("aBlobOfMedia", "trainer_id", MagicMock())
    # Assert data
    assert file == "filename"
    # Assert expectations
    initialize_spy.assert_called_once()
    storage_bucket_spy.assert_called_once()
    get_file_name_stub.assert_called_once_with("trainer_id")


spy_with_data = MagicMock()
spy_with_data.blob = MagicMock(return_value=spy_with_data)
spy_with_data.download_as_text = MagicMock(return_value="blob")


@patch("trainings.firebase.initialize")
@patch("trainings.firebase.storage.bucket", return_value=spy_with_data)
def test_when_getting_media_expect_blob(
    storage_bucket_spy: MagicMock,
    initialize_spy: MagicMock,
):
    # Exercise
    media = read("a_file_name", MagicMock())
    # Assert data
    assert media == "blob"
    # Assert expectations
    initialize_spy.assert_called_once()
    storage_bucket_spy.assert_called_once()
    spy_with_data.blob.assert_called_once_with("a_file_name")
    spy_with_data.download_as_text.assert_called_once()


spy_with_error = MagicMock()
spy_with_error.blob = MagicMock(return_value=spy_with_error)
spy_with_error.download_as_text = MagicMock(side_effect=NotFound("banana"))


@patch("trainings.firebase.initialize")
@patch("trainings.firebase.storage.bucket", return_value=spy_with_error)
def test_when_media_not_found_expect_none(
    storage_bucket_spy: MagicMock,
    initialize_spy: MagicMock,
):
    # Exercise
    media = read("a_file_name", MagicMock())
    # Assert data
    assert not media
    # Assert expectations
    initialize_spy.assert_called_once()
    storage_bucket_spy.assert_called_once()
    spy_with_error.blob.assert_called_once_with("a_file_name")
    spy_with_error.download_as_text.assert_called_once()


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

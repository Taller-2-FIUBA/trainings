# pylint: disable= missing-module-docstring, missing-function-docstring
from os import environ
from unittest.mock import patch
from environ import to_config
from trainings.config import AppConfig


@patch.dict(environ, {}, clear=True)
def test_when_environment_is_empty_expect_9001_prometheus_port():
    cnf = to_config(AppConfig)
    assert cnf.prometheus_port == 9001


@patch.dict(environ, {}, clear=True)
def test_when_environment_is_empty_expect_warning_log_level():
    cnf = to_config(AppConfig)
    assert cnf.log_level == "WARNING"


@patch.dict(environ, {"TRAININGS_PROMETHEUS_PORT": "9004"}, clear=True)
def test_when_environment_has_prometheus_port_9004_expect_9004():
    cnf = to_config(AppConfig)
    assert cnf.prometheus_port == 9004


@patch.dict(environ, {"TRAININGS_LOG_LEVEL": "DEBUG"}, clear=True)
def test_when_environment_debug_log_level_expect_debug():
    cnf = to_config(AppConfig)
    assert cnf.log_level == "DEBUG"


@patch.dict(environ, {"TRAININGS_DB_DRIVER": "postgresql"}, clear=True)
def test_when_environment_db_driver_expect_postgresql():
    cnf = to_config(AppConfig)
    assert cnf.db.driver == "postgresql"


@patch.dict(environ, {"TRAININGS_DB_PASSWORD": "secret"}, clear=True)
def test_when_environment_db_password_expect_secret():
    cnf = to_config(AppConfig)
    assert cnf.db.password == "secret"


@patch.dict(environ, {"TRAININGS_DB_USER": "backend"}, clear=True)
def test_when_environment_db_user_expect_backend():
    cnf = to_config(AppConfig)
    assert cnf.db.user == "backend"


@patch.dict(environ, {"TRAININGS_DB_HOST": "localhost"}, clear=True)
def test_when_environment_db_host_expect_localhost():
    cnf = to_config(AppConfig)
    assert cnf.db.host == "localhost"


@patch.dict(environ, {"TRAININGS_DB_PORT": "5432"}, clear=True)
def test_when_environment_db_port_expect_5432():
    cnf = to_config(AppConfig)
    assert cnf.db.port == 5432


@patch.dict(environ, {"TRAININGS_DB_DATABASE": "fiufit"}, clear=True)
def test_when_environment_db_database_expect_fiufit():
    cnf = to_config(AppConfig)
    assert cnf.db.database == "fiufit"


@patch.dict(environ, {"TRAININGS_DB_CREATE_STRUCTURES": "True"}, clear=True)
def test_when_environment_db_create_structures_expect_true():
    cnf = to_config(AppConfig)
    assert cnf.db.create_structures


@patch.dict(
    environ,
    {"TRAININGS_AUTH_HOST": "auth-service.fiufit.svc.cluster.local:8002"},
    clear=True
)
def test_when_environment_auth_host_expect_auth_service():
    cnf = to_config(AppConfig)
    assert cnf.auth.host == "auth-service.fiufit.svc.cluster.local:8002"


@patch.dict(environ, {}, clear=True)
def test_when_firebase_type_is_empty_expect_service_account():
    cnf = to_config(AppConfig)
    assert cnf.firebase.type == "service_account"


@patch.dict(environ, {"TRAININGS_FIREBASE_TYPE": "fiufit"}, clear=True)
def test_when_firebase_type_has_fiufit_expect_fiufit():
    cnf = to_config(AppConfig)
    assert cnf.firebase.type == "fiufit"


@patch.dict(environ, {}, clear=True)
def test_when_firebase_project_id_is_empty_expect_taller2_fiufit():
    cnf = to_config(AppConfig)
    assert cnf.firebase.project_id == "taller2-fiufit"


@patch.dict(environ, {"TRAININGS_FIREBASE_PROJECT_ID": "an_id"}, clear=True)
def test_when_firebase_project_id_has_an_id_expect_an_id():
    cnf = to_config(AppConfig)
    assert cnf.firebase.project_id == "an_id"


@patch.dict(environ, {}, clear=True)
def test_when_firebase_private_key_id_is_empty_expect_id():
    cnf = to_config(AppConfig)
    assert cnf.firebase.private_key_id ==\
        "404e45eb1856c2152c53e2a805e59b0b186ab956"


@patch.dict(environ, {"TRAININGS_FIREBASE_PRIVATE_KEY_ID": "id"}, clear=True)
def test_when_firebase_private_key_id_has_id_expect_id():
    cnf = to_config(AppConfig)
    assert cnf.firebase.private_key_id == "id"


@patch.dict(environ, {}, clear=True)
def test_when_firebase_private_key_is_empty_expect_default():
    cnf = to_config(AppConfig)
    assert cnf.firebase.private_key == "https://tenor.com/bhDEJ.gif"


@patch.dict(environ, {"TRAININGS_FIREBASE_PRIVATE_KEY": "a_pk"}, clear=True)
def test_when_firebase_private_key_has_a_pk_expect_a_pk():
    cnf = to_config(AppConfig)
    assert cnf.firebase.private_key == "a_pk"


@patch.dict(environ, {}, clear=True)
def test_when_firebase_client_email_is_empty_expect_main():
    cnf = to_config(AppConfig)
    assert cnf.firebase.client_email ==\
        "firebase-adminsdk-zwduu@taller2-fiufit.iam.gserviceaccount.com"


@patch.dict(environ, {"TRAININGS_FIREBASE_CLIENT_EMAIL": "mail"}, clear=True)
def test_when_firebase_client_email_has_mail_expect_mail():
    cnf = to_config(AppConfig)
    assert cnf.firebase.client_email == "mail"


@patch.dict(environ, {}, clear=True)
def test_when_firebase_client_id_is_empty_expect_client_id():
    cnf = to_config(AppConfig)
    assert cnf.firebase.client_id == "117815040269453856692"


@patch.dict(environ, {"TRAININGS_FIREBASE_CLIENT_ID": "12314"}, clear=True)
def test_when_firebase_client_id_has_12314_expect_12314():
    cnf = to_config(AppConfig)
    assert cnf.firebase.client_id == "12314"


@patch.dict(environ, {}, clear=True)
def test_when_firebase_auth_uri_is_empty_expect_auth_uri():
    cnf = to_config(AppConfig)
    assert cnf.firebase.auth_uri == "https://accounts.google.com/o/oauth2/auth"


@patch.dict(environ, {"TRAININGS_FIREBASE_AUTH_URI": "auth.com"}, clear=True)
def test_when_firebase_auth_uri_has_auth_com_expect_auth_com():
    cnf = to_config(AppConfig)
    assert cnf.firebase.auth_uri == "auth.com"


@patch.dict(environ, {}, clear=True)
def test_when_firebase_token_uri_is_empty_expect_token_uri():
    cnf = to_config(AppConfig)
    assert cnf.firebase.token_uri == "https://oauth2.googleapis.com/token"


@patch.dict(environ, {"TRAININGS_FIREBASE_TOKEN_URI": "token.com"}, clear=True)
def test_when_firebase_token_uri_has_token_com_expect_token_com():
    cnf = to_config(AppConfig)
    assert cnf.firebase.token_uri == "token.com"


@patch.dict(environ, {}, clear=True)
def test_when_firebase_auth_provider_x509_cert_url_is_empty_expect_url():
    cnf = to_config(AppConfig)
    assert cnf.firebase.auth_provider_x509_cert_url ==\
        "https://www.googleapis.com/oauth2/v1/certs"


@patch.dict(
    environ,
    {"TRAININGS_FIREBASE_AUTH_PROVIDER_X509_CERT_URL": "cert.com"},
    clear=True
)
def test_when_firebase_auth_provider_x509_cert_url_has_url_expect_cert_com():
    cnf = to_config(AppConfig)
    assert cnf.firebase.auth_provider_x509_cert_url == "cert.com"


@patch.dict(environ, {}, clear=True)
def test_when_firebase_client_x509_cert_url_is_empty_expect_url():
    cnf = to_config(AppConfig)
    assert cnf.firebase.client_x509_cert_url ==\
        "https://www.googleapis.com/robot/v1/metadata/x509/"\
        "firebase-adminsdk-zwduu%40taller2-fiufit.iam.gserviceaccount.com"


@patch.dict(
    environ,
    {"TRAININGS_FIREBASE_CLIENT_X509_CERT_URL": "cert.com"},
    clear=True
)
def test_when_firebase_client_x509_cert_url_has_url_expect_cert_com():
    cnf = to_config(AppConfig)
    assert cnf.firebase.client_x509_cert_url == "cert.com"


@patch.dict(environ, {}, clear=True)
def test_when_firebase_storagebucket_is_empty_expect_url():
    cnf = to_config(AppConfig)
    assert cnf.firebase.storagebucket == "taller2-fiufit.appspot.com"


@patch.dict(
    environ,
    {"TRAININGS_FIREBASE_STORAGEBUCKET": "bucket.com"},
    clear=True
)
def test_when_firebase_storagebucket_has_url_expect_bucket_com():
    cnf = to_config(AppConfig)
    assert cnf.firebase.storagebucket == "bucket.com"

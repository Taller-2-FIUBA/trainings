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
def test_when_firebase_project_id_is_empty_expect_service_account():
    cnf = to_config(AppConfig)
    assert cnf.firebase.project_id == "taller2-fiufit"


@patch.dict(environ, {"TRAININGS_FIREBASE_PROJECT_ID": "an_id"}, clear=True)
def test_when_firebase_project_id_has_an_id_expect_an_id():
    cnf = to_config(AppConfig)
    assert cnf.firebase.project_id == "an_id"


@patch.dict(environ, {}, clear=True)
def test_when_firebase_private_key_id_is_empty_expect_service_account():
    cnf = to_config(AppConfig)
    assert cnf.firebase.private_key_id ==\
        "404e45eb1856c2152c53e2a805e59b0b186ab956"


@patch.dict(environ, {"TRAININGS_FIREBASE_PRIVATE_KEY_ID": "id"}, clear=True)
def test_when_firebase_private_key_id_has_id_expect_id():
    cnf = to_config(AppConfig)
    assert cnf.firebase.private_key_id == "id"

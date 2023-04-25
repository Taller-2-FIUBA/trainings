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

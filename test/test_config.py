import os
import sys
import pytest
import yaml

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import Config, ServerConfig, DatabaseConfig


# Создаем фикстуру для тестовых данных конфигурации
@pytest.fixture
def sample_config_file(tmp_path):
    config_data = {
        "server": {"host": "0.0.0.0", "port": 8080},
        "database": {
            "host": "db_host",
            "port": 5433,
            "user": "db_user",
            "password": "db_password",
            "database": "test_db",
        },
    }

    config_file = tmp_path / "config.yaml"
    with open(config_file, "w") as file:
        yaml.safe_dump(config_data, file)

    return config_file


def test_server_config(sample_config_file):
    config = Config.from_file(sample_config_file)
    server_config = config.server

    assert server_config.host == "0.0.0.0"
    assert server_config.port == 8080


def test_database_config(sample_config_file):
    config = Config.from_file(sample_config_file)
    database_config = config.database

    assert database_config.host == "db_host"
    assert database_config.port == 5433
    assert database_config.user == "db_user"
    assert database_config.password == "db_password"
    assert database_config.database == "test_db"


def test_default_values():
    config_data = {"server": {}, "database": {}}

    with open("default_config.yaml", "w") as file:
        yaml.safe_dump(config_data, file)

    config = Config.from_file("default_config.yaml")
    server_config = config.server
    database_config = config.database

    assert server_config.host == "127.0.0.1"
    assert server_config.port == 8000
    assert database_config.host == "localhost"
    assert database_config.port == 5432
    assert database_config.user == "user"
    assert database_config.password == "password"
    assert database_config.database == "default_db"

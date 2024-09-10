import yaml
from typing import Dict


class ServerConfig:
    def __init__(self, config: Dict[str, str]):
        self.host = config.get("host", "127.0.0.1")
        self.port = config.get("port", 8000)


class DatabaseConfig:
    def __init__(self, config: Dict[str, str]):
        self.host = config.get("host", "localhost")
        self.port = config.get("port", 5432)
        self.user = config.get("user", "user")
        self.password = config.get("password", "password")
        self.database = config.get("database", "default_db")


class Config:
    def __init__(self, server: ServerConfig, database: DatabaseConfig):
        self.server = server
        self.database = database

    @classmethod
    def from_file(cls, file_path: str):
        with open(file_path, "r") as file:
            config_data = yaml.safe_load(file)

        server_config = ServerConfig(config_data["server"])
        database_config = DatabaseConfig(config_data["database"])

        return cls(server_config, database_config)

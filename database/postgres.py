from config import DatabaseConfig
import asyncpg


class Database:
    def __init__(self, db_config: DatabaseConfig):
        self.db_config = db_config
        self.connection = None

    async def connect_to_db(self):
        if self.connection is None:
            self.connection = await asyncpg.connect(
                host=self.db_config.host,
                port=self.db_config.port,
                user=self.db_config.user,
                password=self.db_config.password,
                database=self.db_config.database,
            )
            print("Подключено к базе данных PostgreSQL")
        else:
            print("Уже подключены к базе данных")

    async def disconnect(self):
        """Отключаемся от базы данных PostgreSQL."""
        if self.connection:
            await self.connection.close()
            print("Соединение с базой данных закрыто")
            self.connection = None
        else:
            print("Соединение уже закрыто")

    async def execute_query(self, query: str, *args):
        """Выполняем SQL-запрос и возвращаем результат."""
        if self.connection is None:
            raise Exception("Нет подключения к базе данных.")

        try:
            result = await self.connection.fetch(query, *args)
            return result
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return None

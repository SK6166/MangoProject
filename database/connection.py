from pymongo import MongoClient
from pymongo.errors import OperationFailure, PyMongoError, ServerSelectionTimeoutError
from config import Config

class DatabaseConnection:
    _instances = {}

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.client = None
        self.db = None

    def connect(self):
        try:
            uri = (
                f"mongodb://{self.username}:{self.password}@"
                f"{Config.MONGO_HOST}:{Config.MONGO_PORT}/{Config.MONGO_DB}"
                f"?authSource={Config.MONGO_AUTH_SOURCE}"
                f"&serverSelectionTimeoutMS={Config.SERVER_TIMEOUT}"
                f"&connectTimeoutMS={Config.CONNECT_TIMEOUT}"
            )
            self.client = MongoClient(uri)
            self.client.admin.command('ping')
            self.db = self.client[Config.MONGO_DB]
            return self.db
        except OperationFailure as e:
            raise OperationFailure(f"Ошибка авторизации: {e}")
        except ServerSelectionTimeoutError as e:
            raise Exception(f"Таймаут подключения к серверу MongoDB: {e}")
        except Exception as e:
            raise Exception(f"Ошибка подключения: {e}")

    def close(self):
        if self.client:
            self.client.close()

    @staticmethod
    def get_connection(username, password):
        key = f"{username}:{password}"
        if key not in DatabaseConnection._instances:
            conn = DatabaseConnection(username, password)
            conn.connect()
            DatabaseConnection._instances[key] = conn
        return DatabaseConnection._instances[key]

    @staticmethod
    def close_all():
        for conn in DatabaseConnection._instances.values():
            conn.close()
        DatabaseConnection._instances.clear()
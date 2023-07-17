import os
from logging import config as logging_config

from pydantic import BaseSettings

from core.logger import LOGGING


class ProjectSettings(BaseSettings):
    PROJECT_NAME: str = "Insurance"
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    BACKOFF_MAX_TIME: int = 60

    class Config:
        env_file = ".env"


class PostgresSettings(BaseSettings):
    # Настройки Postgres
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_DATABASE: str = "insurance"
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "pass"

    class Config:
        env_file = ".env"


postgres_settings = PostgresSettings()

TORTOISE_ORM = {
    "connections": {
         "pg": "postgres://{}:{}@{}:{}/{}".format(
             postgres_settings.POSTGRES_USER,
             postgres_settings.POSTGRES_PASSWORD,
             postgres_settings.POSTGRES_HOST,
             postgres_settings.POSTGRES_PORT,
             postgres_settings.POSTGRES_DATABASE,
             )
    },
    "apps": {
        "models": {
            "models": [
                 "models",
                 "aerich.models"
            ],
            "default_connection": "pg",
        },
    },
}


project_settings = ProjectSettings()

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

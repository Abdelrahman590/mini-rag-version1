from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "Mini RAG"
    APP_VERSION: str = "1.0.0"
    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE : int
    FILE_DEFULT_CHUNK_SIZE : int
    DEBUG: bool = True
    model_config = ConfigDict(
        env_file=".env",
       
    )


@lru_cache
def get_settings():
    return Settings()

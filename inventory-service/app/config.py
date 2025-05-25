import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DB_USER: str = os.getenv("DB_USER", "user")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "password")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "3306")
    DB_NAME: str = os.getenv("DB_NAME", "inventory_db")

    # Upload settings
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "app/static/uploads")

    # App
    APP_NAME: str = "Inventory Service"
    DEBUG: bool = True

    class Config:
        env_file = ".env"  # Load biến từ file .env nếu có

settings = Settings()

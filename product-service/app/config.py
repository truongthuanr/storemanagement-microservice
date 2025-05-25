from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+pymysql://user:password@localhost/productdb"

    class Config:
        env_file = ".env"

settings = Settings()

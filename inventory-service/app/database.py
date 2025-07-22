import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from app.config import settings

# Kết nối MySQL dùng PyMySQL
DATABASE_URL = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

# Tạo engine và session factory
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base để dùng cho các ORM model
Base = declarative_base()

# Dependency cho FastAPI
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

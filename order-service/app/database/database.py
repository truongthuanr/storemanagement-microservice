from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings  # load từ .env hoặc config
from sqlalchemy.orm import declarative_base

Base = declarative_base()

DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

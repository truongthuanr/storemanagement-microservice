from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

app = FastAPI()
Base = declarative_base()
engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    books = relationship("Book", back_populates="author")

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="books")

Base.metadata.create_all(bind=engine)

class AuthorCreate(BaseModel):
    name: str

class BookCreate(BaseModel):
    title: str
    author_id: int

@app.post("/authors")
def create_author(author: AuthorCreate):
    db = SessionLocal()
    db_author = Author(name=author.name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

@app.post("/books")
def create_book(book: BookCreate):
    db = SessionLocal()
    db_author = db.query(Author).filter_by(id=book.author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    db_book = Book(title=book.title, author_id=book.author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/books")
def get_books():
    db = SessionLocal()
    return db.query(Book).all()

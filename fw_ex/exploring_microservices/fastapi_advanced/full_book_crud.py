from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from cryptography.fernet import Fernet

app = FastAPI()

# database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./books.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# this is for database
Base = declarative_base()

key = Fernet.generate_key()
print(key)
cipher_suite = Fernet(key)


# Base class is inherited by Book class
class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    isbn = Column(String, unique=True, index=True)
    encrypted_summary = Column(String)


Base.metadata.create_all(bind=engine)

# Create seperate pydantic models for


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    author: str = Field(..., min_length=3, max_length=50)
    isbn: str = Field(..., pattern="^[0-9]{10,13}$", description="10 to 13 digits")
    summary: str


class BookUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    author: str = Field(..., min_length=3, max_length=50)
    summary: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def encrypt_summary(summary: str):
    return cipher_suite.encrypt(summary.encode()).decode()


def decrypt_summary(encrypt_summary: str):
    print("encrypted_summary recieved is:", encrypt_summary)
    return cipher_suite.decrypt(encrypt_summary.encode()).decode()


@app.post("/books/", response_model=BookCreate)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    # query for the book
    db_book = db.query(Book).filter(Book.isbn == book.isbn)
    if not db_book:
        # if book exists then raise error & return
        raise HTTPException(status_code=400, detail="ISBN code exists")
    enc_summary = encrypt_summary(book.summary)
    new_book = Book(
        title=book.title,
        author=book.author,
        isbn=book.isbn,
        encrypted_summary=enc_summary,
    )
    # add, commit and refresh
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return {
        "title": new_book.title,
        "author": new_book.author,
        "isbn": new_book.isbn,
        "summary": new_book.encrypted_summary,
    }


@app.get("/books/")
def read_list(skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    books = db.query(Book).offset(skip).limit(limit).all()
    return [
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "summary": decrypt_summary(book.encrypted_summary),
        }
        for book in books
    ]


@app.put("/books/{book_id}")
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail=f"Book {book_id} not available")
    if book.title:
        db_book.title = book.title
    if book.author:
        db_book.author = book.author
    if book.summary:
        db_book.summary = encrypt_summary(book.summary)
    db.commit()
    db.refresh(db_book)


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = (
        db.query(Book).filter(Book.id == book_id).filter(Book.id == book_id).first()
    )
    if db_book:
        db.delete(db_book)
        db.commit()
        return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Not found")

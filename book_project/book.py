from typing import Optional
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

class Book:
  id: int
  title: str 
  author: str 
  description: str
  rating: int

  def __init__(self, id, title, author, description, rating):
    self.id = id
    self.title = title
    self.author = author
    self.description = description
    self.rating = rating


class BookRequest(BaseModel):
  id: Optional[int] = Field(description="ID is not needed on create", default=None)
  title: str = Field(min_length=3)
  author: str = Field(min_length=3)
  description: str = Field(min_length=1, max_length=200)
  rating: int = Field(gt=0, lt=6)

  model_config = {
    "json_schema_extra": {
      "example": {
        "title": "A new book",
        "author": "adriano",
        "description": "A new description of a book",
        "rating": 5
      }
    }
  }


BOOKS = [
    Book(
        1,
        "To Kill a Mockingbird",
        "Harper Lee",
        "A novel about the serious issues of rape and racial inequality told through the eyes of a child.",
        5
    ),
    Book(
        2,
        "1984",
        "George Orwell",
        "A dystopian novel that explores government surveillance and totalitarianism.",
        5
    ),
    Book(
        3,
        "The Great Gatsby",
        "F. Scott Fitzgerald",
        "A story of the mysterious millionaire Jay Gatsby and his passion for the beautiful Daisy Buchanan.",
        4
    ),
    Book(
        4,
        "Pride and Prejudice",
        "Jane Austen",
        "A romantic novel that also critiques the British landed gentry of the early 19th century.",
        5
    ),
    Book(
        5,
        "Moby-Dick",
        "Herman Melville",
        "The quest of Ishmael and Captain Ahab for the elusive white whale, Moby Dick.",
        4
    ),
    Book(
        6,
        "The Catcher in the Rye",
        "J.D. Salinger",
        "A story about teenage rebellion and alienation through the eyes of Holden Caulfield.",
        4
    )
]


app = FastAPI()

@app.get("/books")
async def read_all_books():
  return BOOKS

@app.get("/books/{book_id}")
async def read_book(book_id: int):
  for book in BOOKS:
    if book_id == book.id:
      return book
 
@app.get("/books/")
async def read_book_by_rating(book_rating: int):
  books_list = []
  for book in BOOKS:
    if book.rating == book_rating:
      books_list.append(book)
  
  return books_list


@app.post("/create-book")
async def create_book(book_request: BookRequest):
  new_book = Book(**book_request.model_dump())
  BOOKS.append(find_book_id(new_book))


def find_book_id(book:Book):
  book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
  return book

@app.put("/books/update_book")
async def update_book(book: BookRequest):
  for i in range(len(BOOKS)):
    if BOOKS[i].id == book.id:
      BOOKS[i] = book

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
  for i in range(len(BOOKS)):
    if BOOKS[i].id == book_id:
      BOOKS.pop(i)
      break
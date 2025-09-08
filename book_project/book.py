from fastapi import FastAPI, Body
from pydantic import BaseModel

class Book:
  id: int
  title: str
  author: str
  description: str
  rating: int

  def __init__(self, id, title, author, description, rating) -> None:
    self.id = id
    self.title = title
    self.author = author
    self.description = description
    self.rating = rating


class BookRequest(BaseModel):
  id: int
  title: str
  author: str
  description: str
  rating: int


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

@app.post("/create-book")
async def create_book(book_request: BookRequest):
  new_book = Book(**book_request.model_dump())
  BOOKS.append(new_book)
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Book:
  id: Optional[int] = None
  title: str
  author: str
  description: str
  rating: float

  def __init__(self, id: int, title: str, author: str, description: str, rating: float):
    self.id = id
    self.title = title
    self.author = author
    self.description = description
    self.rating = rating
    
class BookRequest(BaseModel):
  id: int 
  title: str = Field(min_length=3)
  author: str = Field(min_length=3)
  description: str = Field(min_length=3, max_length=100)
  rating: float = Field(gt=0, lt=6)



BOOKS = [
  Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book', 5),
  Book(2, 'Be Fast with API', 'codingwithroby', 'A great book', 5),
  Book(3, 'Master EndPoints', 'codingwithroby', 'A awesome book', 5),
  Book(4, 'HP1', 'Author 1', 'Book Description', 2),
  Book(5, 'HP2', 'Author 2', 'Book Description', 3),
  Book(6, 'HP3', 'Author 3', 'Book Description', 1)
]

@app.post("/books")
async def read_all_books():
  return BOOKS

@app.post('/create_book')
async def create_book(book_request: BookRequest):
  new_book = Book(**book_request.model_dump())
  BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
  book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
  return book
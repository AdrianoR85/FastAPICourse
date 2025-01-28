from fastapi import FastAPI, Body

app = FastAPI()

class Book:
  id: int
  title: str
  author: str
  category: str
  rating: float

  def __init__(self, id: int, title: str, author: str, category: str, rating: float):
    self.id = id
    self.title = title
    self.author = author
    self.category = category
    self.rating = rating

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
async def create_book(book_request= Body()):
  BOOKS.append(book_request)
from fastapi import FastAPI

BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author three", "category": "history"},
    {"title": "Title Four", "author": "Author Four", "category": "math"},
    {"title": "Title Five", "author": "Author Five", "category": "math"},
    {"title": "Title Six", "author": "Author Two", "category": "math"}
]

app = FastAPI()

@app.get("/books")
async def read_all_books():
  return BOOKS

@app.get("/books/{book_title}")
async def read_book_by_title(book_title: str):
  for book in BOOKS: 
    title = book.get("title")
    if title and title.casefold() == book_title.casefold():
      return book
    
  return {"Failed": "Title not Found"}

@app.get("/books/")
async def read_category_query(book_category: str):
  book_list = []

  for book in BOOKS:
    category = book.get("category")

    if not category:
      return {"Error": "The category is required."}
    
    if category.casefold() == book_category:
      book_list.append(book)

  if book_list:
    return book_list
  else:
    return {"Not Found": "No book were found." }    

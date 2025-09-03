from fastapi import Body, FastAPI

BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author three", "category": "history"},
    {"title": "Title Four", "author": "Author Four", "category": "math"},
    {"title": "Title Five", "author": "Author Five", "category": "math"},
    {"title": "Title Six", "author": "Author Two", "category": "math"}
]

app = FastAPI()


#GET HTTP Methods
""" It is used by clients,such as web browserr, to retrieve informarion from a server."""

@app.get("/books")
async def read_all_books() -> list:
  return BOOKS

@app.get("/books/{book_title}")
async def read_book_by_title(book_title: str) -> dict:
  for book in BOOKS: 
    title = book.get("title")
    if title and title.casefold() == book_title.casefold():
      return book
    
  return {"Failed": "Title not Found"}

@app.get("/books/")
async def read_category_query(book_category: str) -> list | dict:
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

@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, book_category: str) -> list | dict:
  book_list = []

  for book in BOOKS:
    author = book.get("author")
    category = book.get("category")

    if not author and not book_category:
      return {"Failed": "author or category is required"}
    
    if author.casefold() == book_author and category.casefold() == book_category: # type: ignore
      book_list.append(book)
  
  if book_list:
    return book_list
  else:
    return {"Not Found": "No book were found." }  
  

# POST HTTP Methods
"""It is used to send data to a server to create anew resource or submit data for processing."""

@app.post("/books/craete_book")
async def create_book(new_book=Body()):
  BOOKS.append(new_book)
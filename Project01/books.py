from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "history"},
    {"title": "Title Four", "author": "Author Four", "category": "math"},
    {"title": "Title Five", "author": "Author Five", "category": "math"},
    {"title": "Title Six", "author": "Author Six", "category": "science"},
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_title}")
async def read_all_books(book_title: str):
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            return book
        for book in BOOKS:
            if book.get("title").casefold() == book_title.casefold():
                return book


@app.get("/books/{book_author}/")
async def read_category_by_query(book_author: str, category: str):
    books_found = []
    for book in BOOKS:
        if (
            book.get("author").casefold() == book_author.casefold()
            and book.get("category").casefold() == category.casefold()
        ):
            books_found.append(book)
    return books_found


@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)
    return {"message": "Book created successfully"}


@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for book in BOOKS:
        if book.get("title").casefold() == updated_book.get("title").casefold():
            book.update(updated_book)
            return {
                "message": f"Book '{updated_book.get('title')}' updated successfully"
            }


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            BOOKS.remove(book)
            return {"message": f"Book '{book_title}' deleted successfully"}
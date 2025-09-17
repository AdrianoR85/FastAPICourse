# 📘 FastAPI Course

This repository is part of my FastAPI learning course.
Each part of the course builds a small project or feature.

## 👉 Part 2 introduces database integration with SQLAlchemy:
This is a minimal FastAPI + SQLAlchemy project that demonstrates how to:

- Connect to a PostgreSQL database
- Define models (tables) using SQLAlchemy ORM
- Create and query tables through FastAPI endpoints

###  ⚙️ Setup Instructions

####  1. Install dependencies
```bash
  pip install fastapi uvicorn psycopg2-binary sqlalchemy sqlalchemy-utils python-dotenv

```
#### 2. Create a .env file

This file stores database connection settings.

```python
DB_USERNAME=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fastapi_todos

```

#### 3. Files Explained
`database.py`
- Creates the database engine
- Ensures the database exists
- Provides a SessionLocal factory for DB sessions
- Defines Base for ORM models

`models.py`
- Defines the Todos table:
  - id → Primary key
  - title → Task title
  - description → Task details
  - priority → Importance level (integer)
  - complete → Task status (boolean, default False)

`main.py`
- Initializes FastAPI
- Creates tables on startup
- Defines a DB dependency (get_db)
- Provides a sample endpoint (GET /) that returns all todos

---

### Database Session Dependency

In FastAPI, it’s common to use a dependency to manage database sessions. This ensures that each request gets its own session and that connections are always closed properly.

```python
def get_db():
  db = SessionLocal() 
  try:
    yield db 
  finally:
    db.close() 
```

```python
"""Endpoint that queries all todos using that session."""
@app.get("/")
async def read_all(db: Annotated[Session, Depends(get_db)]): 
  return db.query(Todos).all() 
```
#### Explanation
```db = SessionLocal()```
 - Opens a new database session (like creating a "channel" to talk with the database).

```yield db```
- Hands that session to the endpoint (e.g., read_all).
- While the request is running, the session is active and can be used for queries.

```finally: db.close()```
- After the endpoint finishes (whether it succeeds or throws an error), the session is always closed.
- This prevents keeping idle connections open and avoids memory leaks.
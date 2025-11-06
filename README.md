# FastAPI Todo Application

A complete REST API built with FastAPI for managing todo tasks with user authentication and role-based access control.

## What is this project?

This is a **Todo Application API** that allows users to:
- Create an account and log in
- Manage their personal todo tasks (create, read, update, delete)
- Change their password
- Admin users can see and delete all todos from any user

This project was created as part of a FastAPI course to learn how to build modern web APIs with Python.

## Technologies Used

- **FastAPI** - Modern Python web framework for building APIs
- **SQLAlchemy** - Database toolkit and ORM (Object-Relational Mapping)
- **PostgreSQL** - Relational database
- **Alembic** - Database migration tool
- **Pydantic** - Data validation using Python type hints
- **JWT (JSON Web Tokens)** - Secure authentication
- **Passlib with Argon2** - Password hashing for security
- **Python-dotenv** - Environment variable management

## Project Structure

```
├── main.py                 # Main application file
├── database.py            # Database connection setup
├── models.py              # Database table models (Users, Todos)
├── routers/               # API endpoints organized by feature
│   ├── auth.py           # User registration and login
│   ├── todos.py          # Todo CRUD operations
│   ├── admin.py          # Admin-only endpoints
│   └── users.py          # User profile management
├── alembic/              # Database migrations
└── .env                  # Environment variables (you need to create this)
```

## Database Schema

### Users Table
- `id` - Unique user identifier
- `email` - User email (unique)
- `username` - Username (unique)
- `first_name` - User's first name
- `last_name` - User's last name
- `hashed_password` - Encrypted password
- `is_active` - Account status
- `role` - User role (user/admin)
- `phone_number` - Contact number

### Todos Table
- `id` - Unique todo identifier
- `title` - Todo title
- `description` - Todo description
- `priority` - Priority level (1-5)
- `complete` - Completion status
- `owner_id` - Reference to the user who created it

## Setup Instructions

### Prerequisites

Before you start, make sure you have installed:
- Python 3.8 or higher
- PostgreSQL database
- pip (Python package manager)

### Step 1: Clone or Download the Project

Download the project files to your computer.

### Step 2: Install Dependencies

Open your terminal in the project folder and run:

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose passlib argon2-cffi python-dotenv sqlalchemy-utils alembic
```

### Step 3: Create Environment Variables

Create a file named `.env` in the project root folder with these variables:

```
DB_USERNAME=your_postgres_username
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=todoapp
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
```

Replace the values with your PostgreSQL credentials and generate a strong `SECRET_KEY` using `openssl rand -hex 32`.

### Step 4: Run the Application

Start the server with:

```bash
uvicorn main:app --reload
```

The `--reload` flag makes the server restart when you change the code (useful for development).

### Step 5: Access the API Documentation

Open your web browser and go to:

```
http://localhost:8000/docs
```

You will see the **interactive API documentation** where you can test all endpoints.

## API Endpoints

### Authentication (`/auth`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/` | Create a new user account |
| POST | `/auth/token` | Login and get access token |

### Todos (`/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Get all your todos |
| GET | `/todo/{todo_id}` | Get a specific todo |
| POST | `/todo` | Create a new todo |
| PUT | `/todo/{todo_id}` | Update a todo |
| DELETE | `/todo/{todo_id}` | Delete a todo |

### User Management (`/user`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/user/` | Get your user information |
| PUT | `/user/password` | Change your password |

### Admin Only (`/admin`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/Todo` | Get all todos from all users |
| DELETE | `/admin/Todo/{todo_id}` | Delete any todo |

## How to Use the API

### 1. Create a User Account

Send a POST request to `/auth/` with this data:

```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "password": "mypassword123",
  "role": "user"
}
```

### 2. Login

Send a POST request to `/auth/token` with:
- **username**: your username
- **password**: your password

You will receive an **access token**. Copy this token.

### 3. Use the Token

For all other requests, you need to include the token in the **Authorization** header:

```
Authorization: Bearer your_access_token_here
```

In the interactive docs (`/docs`), click the **Authorize** button and paste your token.

### 4. Create a Todo

Send a POST request to `/todo` with:

```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": 3,
  "complete": false
}
```

## Security Features

- **Password Hashing**: Passwords are encrypted using Argon2 (very secure)
- **JWT Authentication**: Tokens expire after 20 minutes
- **Role-Based Access**: Admin users have special permissions
- **Owner Verification**: Users can only see and modify their own todos

---

## Understanding the Code

### 1. Database Connection (database.py)

The database connection is the bridge between your Python code and PostgreSQL.

**How it works:**

```python
# Import necessary tools from SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Load environment variables from .env file
from dotenv import load_dotenv
import os

load_dotenv()

# Build the database URL from environment variables
# Format: postgresql+psycopg2://username:password@host:port/database_name
SQLALCHEMY_DATABASE_URL = (
  f'postgresql+psycopg2://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}'
  f'@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'
)

# Create the database engine (manages the connection pool)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory (sessions are used to interact with the database)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all database models
Base = declarative_base()
```

**Key concepts:**

- **Engine**: Manages the connection to the database
- **Session**: A workspace for database operations (like a transaction)
- **Base**: Parent class for all table models
- **autocommit=False**: Changes are not saved automatically (you must call `db.commit()`)
- **autoflush=False**: Changes are not sent to the database until you commit

**Why use sessions?**

Sessions help manage database transactions safely. If something goes wrong, you can rollback changes without affecting the database.

---

### 2. Creating Models (models.py)

Models are Python classes that represent database tables. SQLAlchemy converts these classes into actual SQL tables.

**Example - Users Model:**

```python
from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class Users(Base):
    __tablename__ = 'users'  # Name of the table in the database
    
    # Define columns (each attribute becomes a column)
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    phone_number = Column(String)
```

**Key concepts:**

- **Column**: Defines a column in the table
- **Integer, String, Boolean**: Data types
- **primary_key=True**: This column is the unique identifier
- **index=True**: Creates an index for faster searches
- **unique=True**: No two rows can have the same value
- **default=True**: Default value if none is provided

**Example - Todos Model with Foreign Key:**

```python
class Todos(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('users.id'))  # Links to Users table
```

**Foreign Key explained:**

`ForeignKey('users.id')` creates a relationship between tables. Each todo is linked to a user through `owner_id`. This ensures that every todo belongs to a specific user.

---

### 3. Authentication System (routers/auth.py)

Authentication verifies who the user is and protects endpoints from unauthorized access.

**Step 1: Password Hashing**

Never store passwords in plain text. We use **Argon2** to hash passwords.

```python
from passlib.context import CryptContext

# Create a password context using Argon2 algorithm
pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')

# Hash a password
hashed_password = pwd_context.hash("mypassword123")
# Result: $argon2id$v=19$m=65536,t=3,p=4$... (long encrypted string)

# Verify a password
is_correct = pwd_context.verify("mypassword123", hashed_password)
# Result: True if password matches, False otherwise
```

**Why Argon2?**

Argon2 is one of the most secure hashing algorithms. Even if someone steals your database, they cannot reverse the hash to get the original password.

**Step 2: Creating JWT Tokens**

When a user logs in, we give them a **JWT token** that proves their identity.

```python
from jose import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = os.getenv("SECRET_KEY")  # Keep this secret!
ALGORITHM = os.getenv("ALGORITHM")

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    # Data to encode in the token
    encode = {'sub': username, 'id': user_id, 'role': role}
    
    # Set expiration time
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    
    # Create the token
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
```

**Token structure:**

A JWT token has three parts separated by dots:
```
header.payload.signature
```

- **Header**: Algorithm information
- **Payload**: User data (username, id, role, expiration)
- **Signature**: Ensures the token was not tampered with

**Step 3: Verifying Tokens**

Every protected endpoint checks if the token is valid.

```python
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from fastapi import HTTPException, status

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Extract user information
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        
        # Check if data exists
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        
        return {'username': username, 'id': user_id, 'role': user_role}
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
```

**How authentication works in endpoints:**

```python
@router.get("/")
async def get_todos(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    # user contains: {'username': 'john_doe', 'id': 1, 'role': 'user'}
    # Only authenticated users can access this endpoint
    return db.query(Todos).filter(Todos.owner_id == user['id']).all()
```

---

### 4. Database Migrations with Alembic

**What are migrations?**

Migrations are version control for your database schema. When you change your models (add a column, create a table, etc.), you need to update the database structure. Alembic helps you do this safely.

**How Alembic is configured:**

**File: alembic/env.py**

This file connects Alembic to your database and models.

```python
from alembic import context
import models
import os
from dotenv import load_dotenv

load_dotenv()

# Get database credentials from .env
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Build the database URL
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Tell Alembic where the database is
config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)

# Tell Alembic about your models (so it can detect changes)
target_metadata = models.Base.metadata
```

**Creating a migration:**

When you change a model, create a migration:

```bash
alembic revision -m "add phone number column to users"
```

This creates a new file in `alembic/versions/` with two functions:

```python
def upgrade() -> None:
    """Apply the change to the database."""
    op.add_column("users", sa.Column('phone_number', sa.String(), nullable=True))

def downgrade() -> None:
    """Undo the change (rollback)."""
    op.drop_column("users", "phone_number")
```

**Applying migrations:**

```bash
alembic upgrade head
```

This runs all pending migrations and updates your database.

**Why use migrations?**

- **Version control**: Track all database changes over time
- **Team collaboration**: Share database changes with your team
- **Rollback**: Undo changes if something goes wrong
- **Production safety**: Apply changes to production databases without manual SQL

**Common Alembic commands:**

```bash
# Create a new migration
alembic revision -m "description"

# Auto-generate migration from model changes
alembic revision --autogenerate -m "description"

# Apply all migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# See migration history
alembic history

# See current version
alembic current
```

---

## Advanced Concepts Explained

### 5. Dependency Injection in FastAPI

**What is Dependency Injection?**

Dependency Injection is a design pattern where you "inject" (provide) dependencies into functions instead of creating them inside the function. FastAPI makes this very easy with the `Depends()` function.

**Example: Database Session Dependency**

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from database import SessionLocal

def get_db():
    """Create and manage database sessions."""
    db = SessionLocal()  # Create a new database session
    try:
        yield db  # Provide this session to the endpoint
    finally:
        db.close()  # Always close the session when done

# Use the dependency in an endpoint
@router.get("/")
async def read_todos(db: Session = Depends(get_db)):
    return db.query(Todos).all()
```

**Why use `yield` instead of `return`?**

- `yield` pauses the function and gives control back to the endpoint
- After the endpoint finishes, the code after `yield` runs (closing the database)
- This ensures the database connection is always closed, even if an error occurs

**Example: User Authentication Dependency**

```python
from typing import Annotated

# Create a reusable type annotation
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/")
async def read_todos(user: user_dependency, db: Session = Depends(get_db)):
    # FastAPI automatically calls get_current_user() and get_db()
    # If authentication fails, the endpoint is never called
    return db.query(Todos).filter(Todos.owner_id == user['id']).all()
```

**Benefits of Dependency Injection:**

1. **Code reuse**: Write the logic once, use it everywhere
2. **Automatic validation**: Dependencies run before the endpoint
3. **Clean code**: Endpoints focus on business logic, not setup
4. **Easy testing**: You can replace dependencies with mock versions

---

### 6. Data Validation with Pydantic

**What is Pydantic?**

Pydantic is a library that validates data using Python type hints. FastAPI uses Pydantic to automatically validate request data.

**Example: Todo Request Model**

```python
from pydantic import BaseModel, Field

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)  # gt = greater than, lt = less than
    complete: bool
```

**What happens when you use this model?**

```python
@router.post("/todo")
async def create_todo(todo_request: TodoRequest):
    # FastAPI automatically:
    # 1. Reads the JSON from the request body
    # 2. Validates each field according to the rules
    # 3. Converts the data to the correct types
    # 4. Returns a 422 error if validation fails
    pass
```

**Validation rules you can use:**

```python
from pydantic import BaseModel, Field, EmailStr

class UserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr  # Must be a valid email format
    age: int = Field(ge=18, le=120)  # ge = greater or equal, le = less or equal
    password: str = Field(min_length=8)
    website: str | None = None  # Optional field
```

**Converting Pydantic models to dictionaries:**

```python
todo_request = TodoRequest(
    title="Buy milk",
    description="From the store",
    priority=3,
    complete=False
)

# Convert to dictionary
todo_dict = todo_request.model_dump()
# Result: {'title': 'Buy milk', 'description': 'From the store', ...}

# Use with SQLAlchemy models
todo_model = Todos(**todo_dict, owner_id=1)
```

---

### 7. Error Handling and HTTP Status Codes

**HTTP Status Codes Used in This Project:**

| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 | OK | Successful GET request |
| 201 | Created | Successfully created a resource |
| 204 | No Content | Successful DELETE or UPDATE (no data returned) |
| 400 | Bad Request | Invalid data format |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | User doesn't have permission |
| 404 | Not Found | Resource doesn't exist |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server error |

**Raising HTTP Exceptions:**

```python
from fastapi import HTTPException, status

@router.get("/todo/{todo_id}")
async def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    
    if todo is None:
        # Raise an exception with a custom message
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found."
        )
    
    return todo
```

**Custom Error Responses:**

```python
# You can return detailed error information
raise HTTPException(
    status_code=400,
    detail={
        "error": "Invalid priority",
        "message": "Priority must be between 1 and 5",
        "received": priority
    }
)
```

---

### 8. Database Operations (CRUD)

**CRUD** stands for Create, Read, Update, Delete - the four basic operations for any database.

**Create (INSERT):**

```python
@router.post("/todo")
async def create_todo(todo_request: TodoRequest, db: Session = Depends(get_db)):
    # Create a new instance of the model
    new_todo = Todos(
        title=todo_request.title,
        description=todo_request.description,
        priority=todo_request.priority,
        complete=todo_request.complete,
        owner_id=1
    )
    
    # Add to the session (not saved yet)
    db.add(new_todo)
    
    # Save to the database
    db.commit()
    
    # Refresh to get the auto-generated ID
    db.refresh(new_todo)
    
    return new_todo
```

**Read (SELECT):**

```python
# Get all todos
todos = db.query(Todos).all()

# Get one todo by ID
todo = db.query(Todos).filter(Todos.id == 1).first()

# Get todos with conditions
todos = db.query(Todos)\
    .filter(Todos.complete == False)\
    .filter(Todos.priority > 3)\
    .all()

# Get with ordering
todos = db.query(Todos).order_by(Todos.priority.desc()).all()

# Get with limit
todos = db.query(Todos).limit(10).all()
```

**Update (UPDATE):**

```python
@router.put("/todo/{todo_id}")
async def update_todo(todo_id: int, todo_request: TodoRequest, db: Session = Depends(get_db)):
    # Find the todo
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Update the fields
    todo.title = todo_request.title
    todo.description = todo_request.description
    todo.priority = todo_request.priority
    todo.complete = todo_request.complete
    
    # Save changes
    db.add(todo)
    db.commit()
```

**Delete (DELETE):**

```python
@router.delete("/todo/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    # Find and delete in one query
    result = db.query(Todos).filter(Todos.id == todo_id).delete()
    
    if result == 0:  # No rows were deleted
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.commit()
```

---

### 9. API Router Organization

**Why use APIRouter?**

Instead of putting all endpoints in `main.py`, we organize them into separate files using `APIRouter`. This makes the code easier to maintain.

**Creating a router (routers/todos.py):**

```python
from fastapi import APIRouter

router = APIRouter(
    prefix="/todos",  # All routes start with /todos
    tags=["todos"]    # Group in API documentation
)

@router.get("/")  # Full path: /todos/
async def get_todos():
    pass

@router.post("/")  # Full path: /todos/
async def create_todo():
    pass
```

**Including routers in main.py:**

```python
from fastapi import FastAPI
from routers import auth, todos, admin, users

app = FastAPI()

# Include all routers
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
```

**Benefits:**

- **Separation of concerns**: Each file handles one feature
- **Team collaboration**: Multiple developers can work on different routers
- **Easier testing**: Test each router independently
- **Better documentation**: Routes are grouped logically in the docs

---

### 10. Environment Variables and Security

**Why use environment variables?**

Never hardcode sensitive information (passwords, secret keys) in your code. Use environment variables instead.

**Setting up .env file:**

```env
# Database credentials
DB_USERNAME=postgres
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=todoapp

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
```

**Loading environment variables:**

```python
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Access variables
db_username = os.getenv("DB_USERNAME")
secret_key = os.getenv("SECRET_KEY")

# Provide default values
debug_mode = os.getenv("DEBUG", "False") == "True"
```

**Security best practices:**

1. **Never commit .env to Git**: Add `.env` to `.gitignore`
2. **Use strong SECRET_KEY**: Generate with `openssl rand -hex 32`
3. **Different keys for production**: Never use development keys in production
4. **Rotate keys regularly**: Change secret keys periodically
5. **Use HTTPS in production**: Encrypt data in transit

---

## Development Tips and Best Practices

### Testing Your API

**Using the Interactive Docs:**

1. Go to `http://localhost:8000/docs`
2. Click on any endpoint to expand it
3. Click "Try it out"
4. Fill in the parameters
5. Click "Execute"
6. See the response

**Using curl (command line):**

```bash
# Create a user
curl -X POST "http://localhost:8000/auth/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "password123",
    "role": "user"
  }'

# Login
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=password123"

# Use the token
curl -X GET "http://localhost:8000/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Using Python requests:**

```python
import requests

# Login
response = requests.post(
    "http://localhost:8000/auth/token",
    data={"username": "testuser", "password": "password123"}
)
token = response.json()["access_token"]

# Get todos
response = requests.get(
    "http://localhost:8000/",
    headers={"Authorization": f"Bearer {token}"}
)
todos = response.json()
```

---

### Common Development Patterns

**Pattern 1: Checking ownership before operations**

```python
@router.put("/todo/{todo_id}")
async def update_todo(
    todo_id: int,
    todo_request: TodoRequest,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Find the todo and verify ownership in one query
    todo = db.query(Todos)\
        .filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user['id'])\
        .first()
    
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Update logic here
```

**Pattern 2: Reusable query functions**

```python
def get_todo_by_id(db: Session, todo_id: int, user_id: int):
    """Reusable function to get a todo with ownership check."""
    return db.query(Todos)\
        .filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user_id)\
        .first()

@router.get("/todo/{todo_id}")
async def read_todo(
    todo_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    todo = get_todo_by_id(db, todo_id, user['id'])
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo
```

**Pattern 3: Response models**

```python
from pydantic import BaseModel

class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: int
    complete: bool
    
    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy models

@router.get("/", response_model=list[TodoResponse])
async def get_todos(db: Session = Depends(get_db)):
    # FastAPI automatically converts SQLAlchemy models to TodoResponse
    return db.query(Todos).all()
```

---

### Debugging Tips

**Enable detailed error messages:**

```python
# In main.py
from fastapi import FastAPI

app = FastAPI(debug=True)  # Shows detailed errors (only for development!)
```

**Add logging:**

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/todo")
async def create_todo(todo_request: TodoRequest, db: Session = Depends(get_db)):
    logger.info(f"Creating todo: {todo_request.title}")
    # Your code here
    logger.info(f"Todo created successfully")
```

**Check database queries:**

```python
# Enable SQLAlchemy query logging
from sqlalchemy import create_engine

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)  # Prints all SQL queries
```

---

### Performance Tips

**1. Use database indexes:**

```python
class Todos(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'), index=True)  # Index for faster queries
```

**2. Limit query results:**

```python
# Instead of loading all todos
todos = db.query(Todos).all()  # Could be thousands of rows

# Use pagination
todos = db.query(Todos).limit(20).offset(0).all()  # Only 20 rows
```

**3. Use async database drivers (advanced):**

For better performance with many concurrent users, consider using async database drivers like `asyncpg` with SQLAlchemy's async support.

---

### Project Extension Ideas

Once you understand this project, try adding these features:

**Easy:**
1. Add a `created_at` timestamp to todos
2. Add a search endpoint to find todos by title
3. Add a "mark as complete" endpoint
4. Add todo categories/tags

**Medium:**
5. Add pagination to the get all todos endpoint
6. Add sorting options (by priority, date, etc.)
7. Add email verification when users register
8. Add password reset functionality
9. Add profile pictures for users

**Advanced:**
10. Add todo sharing between users
11. Add real-time notifications with WebSockets
12. Add file attachments to todos
13. Add a frontend with React or Vue.js
14. Deploy to a cloud platform (Heroku, AWS, etc.)

---

## Useful Commands Reference

```bash
# Start the development server
uvicorn main:app --reload

# Start on a different port
uvicorn main:app --reload --port 8080

# Create a new Alembic migration
alembic revision -m "description of change"

# Auto-generate migration from model changes
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1

# See migration history
alembic history

# Install all dependencies
pip install -r requirements.txt

# Create requirements.txt
pip freeze > requirements.txt
```

---

**Happy Coding!** If you have questions, review the code comments - they explain what each part does.

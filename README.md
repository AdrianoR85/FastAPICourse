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
```

Replace the values with your PostgreSQL credentials.

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

SECRET_KEY = "your-secret-key-here"  # Keep this secret!
ALGORITHM = "HS256"

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

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        
        # Extract user information
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        
        # Check if data exists
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="Could not validate user")
        
        return {'username': username, 'id': user_id, 'role': user_role}
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate user")
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

## Common Issues and Solutions

### Problem: "Database does not exist"
**Solution**: The application automatically creates the database if it doesn't exist. Make sure PostgreSQL is running and your credentials in `.env` are correct.

### Problem: "Could not validate user"
**Solution**: Your token might be expired (tokens last 20 minutes). Login again to get a new token.

### Problem: "Authentication Failed"
**Solution**: Make sure you included the token in the Authorization header.

### Problem: "Alembic can't find models"
**Solution**: Make sure `alembic/env.py` imports your models correctly: `import models`

## Learning Resources

If you want to learn more about the technologies used:

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **SQLAlchemy Tutorial**: https://docs.sqlalchemy.org/en/20/tutorial/
- **JWT Basics**: https://jwt.io/introduction
- **Alembic Documentation**: https://alembic.sqlalchemy.org/

## Next Steps

After understanding this project, you can:
1. Add more fields to the todo model (due date, tags, etc.)
2. Create a frontend application to use this API
3. Add email verification for new users
4. Implement todo sharing between users
5. Add file attachments to todos

## License

This project is for educational purposes. Feel free to use it to learn and practice.

---

**Happy Coding!** If you have questions, review the code comments - they explain what each part does.

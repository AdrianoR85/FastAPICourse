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

## Database Migrations

This project uses **Alembic** for database migrations. Migrations help you change the database structure safely.

To create a new migration:

```bash
alembic revision -m "description of changes"
```

To apply migrations:

```bash
alembic upgrade head
```

## Common Issues and Solutions

### Problem: "Database does not exist"
**Solution**: The application automatically creates the database if it doesn't exist. Make sure PostgreSQL is running and your credentials in `.env` are correct.

### Problem: "Could not validate user"
**Solution**: Your token might be expired (tokens last 20 minutes). Login again to get a new token.

### Problem: "Authentication Failed"
**Solution**: Make sure you included the token in the Authorization header.

## Learning Resources

If you want to learn more about the technologies used:

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **SQLAlchemy Tutorial**: https://docs.sqlalchemy.org/en/20/tutorial/
- **JWT Basics**: https://jwt.io/introduction

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

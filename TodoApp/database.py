from sqlalchemy import create_engine   # Import function to create a database engine (manages DB connection)
from sqlalchemy.orm import sessionmaker  # Import sessionmaker to create session objects for DB interaction
from sqlalchemy.ext.declarative import declarative_base  # Import helper to define ORM models (tables)

# Database connection URL (using SQLite, storing data in a local file 'todos.db')
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# Create a database engine (responsible for actual DB connection)
# connect_args={"check_same_thread": False} is required only for SQLite
# It allows the same connection to be used across multiple threads (useful in web apps).
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session factory for interacting with the database
# autocommit=False → transactions need to be committed manually
# autoflush=False → changes are not automatically flushed to the DB until commit/flush
# bind=engine → sessions created will be bound to our engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our ORM models
# Any table model we define will inherit from this Base class
Base = declarative_base()

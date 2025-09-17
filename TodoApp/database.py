from sqlalchemy import create_engine   # Import function to create a database engine (manages DB connection)
from sqlalchemy.orm import sessionmaker  # Import sessionmaker to create session objects for DB interaction
from sqlalchemy.ext.declarative import declarative_base  # Import helper to define ORM models (tables)

from sqlalchemy_utils import database_exists, create_database  # Import helpers to check/create database automatically

from dotenv import load_dotenv  # Import dotenv to load environment variables from .env file
import os  # Import os to access environment variables

load_dotenv()  # Load environment variables from the .env file into the application

# Database connection URL (using PostgreSQL in this case, built from environment variables)
# Format: postgresql+psycopg2://username:password@host:port/databasename
SQLALCHEMY_DATABASE_URL = (
  f'postgresql+psycopg2://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'
)

# Create a database engine (responsible for actual DB connection)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Ensure the database exists (create it if it doesn’t)
if not database_exists(engine.url):
  create_database(engine.url)
  print(f"Database {os.getenv('DB_NAME')} created!")

# Create a session factory for interacting with the database
# autocommit=False → transactions need to be committed manually
# autoflush=False → changes are not automatically flushed to the DB until commit/flush
# bind=engine → sessions created will be bound to our engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our ORM models
# Any table model we define (e.g., User, Todo) will inherit from this Base class
Base = declarative_base()

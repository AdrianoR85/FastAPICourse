from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from ..database import Base
from ..main import app
from ..models import Todos, Users
from ..routers.auth import pwd_context
import pytest


SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
  SQLALCHEMY_DATABASE_URL,
  connect_args={"check_same_thread": False},
  poolclass = StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
  db = TestingSessionLocal()
  try:
    yield db
  finally:
    db.close()

def override_get_current_user():
  return {'usename': 'larac', 'id': 1, 'user_role': 'admin'}

client = TestClient(app)

@pytest.fixture
def test_todo():
  todo = Todos(
    title='Learn to code!',
    description='Need to learn everyday',
    priority=5,
    complete=False,
    owner_id=1
  )

  db = TestingSessionLocal()
  db.add(todo)
  db.commit()
  yield todo
  with engine.connect() as connection:
    connection.execute(text('DELETE FROM todos;'))
    connection.commit()

@pytest.fixture
def test_user():
  hashed = pwd_context.hash("testpassword")
  user = Users( 
    username='larac', 
    email='lara@gmail.com', 
    first_name='Lara', 
    last_name='Croft',
    hashed_password=hashed, 
    role='admin', 
    phone_number='(111)-111-1111' 
  )

  db = TestingSessionLocal()
  db.add(user)
  db.commit()
  yield user
  with engine.connect() as connection:
    connection.execute(text('DELETE FROM users;'))
    connection.commit()
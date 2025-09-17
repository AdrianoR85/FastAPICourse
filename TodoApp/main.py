from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from database import engine, SessionLocal
from models import Todos
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

"""Dependency that manages DB sessions."""
def get_db():
  db = SessionLocal() # Create a new database session (connection)
  try:
    yield db # instead of return db. Provide this session to the endpoint that depends on it
  finally:
    db.close() # After the request is done, close the session to free resources


"""Endpoint that queries all todos using that session."""
@app.get("/")
# - Depends(get_db) tells FastAPI: “Before calling read_all, call get_db() and give me the result.
# - Annotated[Session, Depends(get_db)] means db will be a SQLAlchemy Session
async def read_all(db: Annotated[Session, Depends(get_db)]): 
  return db.query(Todos).all() # uns SELECT * FROM todos; and returns a list of all rows in the todos table.
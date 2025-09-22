from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from database import SessionLocal
from starlette import status
from models import Todos

router = APIRouter()

"""Dependency that manages DB sessions."""
def get_db():
  db = SessionLocal() # Create a new database session (connection)
  try:
    yield db # instead of return db. Provide this session to the endpoint that depends on it
  finally:
    db.close() # After the request is done, close the session to free resources

# - Depends(get_db) tells FastAPI: “Before calling read_all, call get_db() and give me the result.
# - Annotated[Session, Depends(get_db)] means db will be a SQLAlchemy Session
db_dependency = Annotated[Session, Depends(get_db)]


class TodoRequest(BaseModel):
  title: str = Field(min_length=3)
  description: str = Field(min_length=3, max_length=100)
  priority: int = Field(gt=0, lt=6)
  complete: bool


"""Endpoint that queries all todos using that session."""
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency ): 
  return db.query(Todos).all() # uns SELECT * FROM todos; and returns a list of all rows in the todos table.

@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
  todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
  if todo_model is not None:
    return todo_model
  
  raise HTTPException(status_code=404, detail="Todo not found.")


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
  todo_model = Todos(**todo_request.model_dump())

  db.add(todo_model)
  db.commit()


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, 
                      todo_request: TodoRequest,
                      todo_id: int = Path(gt=0)): 
  todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

  if todo_model is None:
    raise HTTPException(status_code=404, detail="Todo not found")
  
  todo_model.title = todo_request.title # type: ignore
  todo_model.description = todo_request.description # type: ignore
  todo_model.complete = todo_request.complete # type: ignore
  todo_model.priority = todo_request.priority # type: ignore

  db.add(todo_model)
  db.commit()

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
  todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

  if todo_model is None:
    raise HTTPException(status_code=404, detail="Todo not found.")
  
  db.query(Todos).filter(Todos.id == todo_id).delete()

  db.commit()
  
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Request
from fastapi.templating import Jinja2Templates
from starlette import status
from starlette.responses import RedirectResponse
from ..database import SessionLocal
from ..models import Todos
from .auth import get_current_user

templates = Jinja2Templates(directory="TodoApp/templates")

router = APIRouter(
  prefix='/todos',
  tags=['todos']
)

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
user_dependecy = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
  title: str = Field(min_length=3)
  description: str = Field(min_length=3, max_length=100)
  priority: int = Field(gt=0, lt=6)
  complete: bool


def redirect_to_login():
  redirect_response = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
  redirect_response.delete_cookie(key="access_token")
  return redirect_response


"""Endpoint that queries all todos using that session."""
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependecy, db: db_dependency ): 
  if user is None:
    raise HTTPException(status_code=401, detail="Authentication Failed.")

  return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()  # uns SELECT * FROM todos; and returns a list of all rows in the todos table.

### Pages ###
@router.get("/todo-page")
async def render_todo_page(request: Request, db: db_dependency):
  try:
    user = await get_current_user(request.cookies.get('access_token')) # type: ignore
    if user is None:
      return redirect_to_login()
    
    todos = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()

    return templates.TemplateResponse("todo.html", {"request": request, "todos": todos, "user": user})
  except:
    return redirect_to_login()
  

@router.get("/add-todo-page")
async def render_add_todo_page(request: Request):
  try:
    user = user = await get_current_user(request.cookies.get('access_token')) # type: ignore

    if user is None:
      return redirect_to_login()
    
    return templates.TemplateResponse("add-todo.html", {"request": request, "user": user})
  except:
    return redirect_to_login()

@router.get("/edit-todo-page/{todo_id}")
async def render_edit_todo_page(request: Request, todo_id: int, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token')) # type: ignore

        if user is None:
            return redirect_to_login()

        todo = db.query(Todos).filter(Todos.id == todo_id).first()

        return templates.TemplateResponse("edit-todo.html", {"request": request, "todo": todo, "user": user})

    except:
        return redirect_to_login()

### Endpoints ###
@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependecy ,db: db_dependency, todo_id: int = Path(gt=0)):
  if user is None:
    raise HTTPException(status_code=401, detail="Authentication Failed.")

  todo_model = db.query(Todos)\
    .filter(Todos.id == todo_id)\
    .filter(Todos.owner_id == user.get('id'))\
    .first()
  if todo_model is not None:
    return todo_model
  
  raise HTTPException(status_code=404, detail="Todo not found.")


@router.post("/todo/", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependecy, db: db_dependency, todo_request: TodoRequest):
  
  if user is None:
    raise HTTPException(status_code=401, detail="Authentication Failed.")
  
  todo_model = Todos(**todo_request.model_dump(), owner_id=user.get('id'))

  db.add(todo_model)
  db.commit()


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependecy,
                      db: db_dependency, 
                      todo_request: TodoRequest,
                      todo_id: int = Path(gt=0)): 
  
  if user is None:
    raise HTTPException(status_code=401, detail="Authentication Failed.")

  todo_model = db.query(Todos)\
    .filter(Todos.id == todo_id)\
    .filter(Todos.owner_id == user.get("id"))\
    .first()
  if todo_model is None:
    raise HTTPException(status_code=404, detail="Todo not found")
  
  todo_model.title = todo_request.title # type: ignore
  todo_model.description = todo_request.description # type: ignore
  todo_model.complete = todo_request.complete # type: ignore
  todo_model.priority = todo_request.priority # type: ignore

  db.add(todo_model)
  db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependecy, db: db_dependency, todo_id: int = Path(gt=0)):
  if user is None:
    raise HTTPException(status_code=401, detail="Authentication Failed.")
  
  todo_model = db.query(Todos).filter(Todos.id == todo_id)\
    .filter(Todos.owner_id == user.get("id"))\
    .first()
  if todo_model is None:
    raise HTTPException(status_code=404, detail="Todo not found.")
  
  db.query(Todos)\
    .filter(Todos.id == todo_id)\
    .filter(Todos.owner_id == user.get("id"))\
    .delete()

  db.commit()
  
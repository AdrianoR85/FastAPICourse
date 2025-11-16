from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from ..database import SessionLocal
from starlette import status
from ..models import Todos, Users
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
  prefix="/user",
  tags=["user"]
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
pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')

class UserVerification(BaseModel):
  password: str
  new_password: str = Field(min_length=6)

@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user:user_dependecy, db: db_dependency):
  if user is None:
    raise HTTPException(status_code=401, detail="Authentication Failed")
  
  return db.query(Users).filter(Users.id == user.get("id")).first()


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependecy, 
    db: db_dependency, 
    user_verification: UserVerification
):
  if user is None:
    raise HTTPException(status_code=401, detail="Authentication Failed")
  
  user_model = db.query(Users).filter(Users.id == user.get("id")).first()

  if user_model is None:
    raise HTTPException(status_code=404, detail="User not found.")
  
  if not pwd_context.verify(user_verification.password, user_model.hashed_password): # type: ignore
    raise HTTPException(status_code=401, detail="Current password is incorrect")
  
  user_model.hashed_password = pwd_context.hash(user_verification.new_password) # type: ignore
  db.add(user_model)
  db.commit()

  return {"message": "Password updated successfully"}

@router.put("/phonenumber/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependecy, db: db_dependency, phone_number: str):
  if user is None:
    raise HTTPException(status_code=401, detail="Authentication Failed")
  
  user_model = db.query(Users).filter(Users.id == user.get("id")).first()
  user_model.phone_number = phone_number # type: ignore
  db.add(user_model)
  db.commit()
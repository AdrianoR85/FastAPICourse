from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

router = APIRouter()

SECRET_KEY = "812a56af29e9b761ede2838870f165da1ddb7d36c8559195141009e770b1be2b"
ALGORITH = "HS256"


pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')

class CreateUserRequest(BaseModel):
  username: str
  email: str
  first_name: str
  last_name: str
  password:str
  role: str


class Token(BaseModel):
  access_token: str
  token_type: str


def get_db():
  db = SessionLocal() 
  try:
    yield db
  finally:
    db.close() 

db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(username: str, password: str, db):
  user = db.query(Users).filter(Users.username == username).first()
  if not user:
    return False
  if not pwd_context.verify(password, user.hashed_password):
    return False
  return user


def craete_access_token(username:str, user_id: int, expires_date: timedelta):
  encode = {'sub': username, 'id': user_id}
  expires = expires = datetime.now(timezone.utc) + expires_date + expires_date

  encode.update({'exp': expires})
  
  return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITH)


@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, 
                      create_user_request: CreateUserRequest):
  
  create_user_model = Users(
    username=create_user_request.username,
    email=create_user_request.email,
    first_name=create_user_request.first_name,
    last_name=create_user_request.last_name,
    role=create_user_request.role,
    hashed_password=pwd_context.hash(create_user_request.password),
    is_active=True
  )

  db.add(create_user_model)
  db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
  
  user = authenticate_user(form_data.username, form_data.password, db)
  if not user:
    return "Failed Authentication"
  
  token = craete_access_token(user.username, user.id, timedelta(minutes=20)) # type: ignore
  return {'access_token': token, 'token_type': 'bearer'}  
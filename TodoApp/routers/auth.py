from fastapi import APIRouter
from pydantic import BaseModel, Field
from models import Users
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')

class CreateUserRequest(BaseModel):
  username: str
  email: str
  first_name: str
  last_name: str
  password:str
  role: str

@router.post("/auth")
async def create_user(create_user_request: CreateUserRequest):
  create_user_model = Users(
    username=create_user_request.username,
    email=create_user_request.email,
    first_name=create_user_request.first_name,
    last_name=create_user_request.last_name,
    role=create_user_request.role,
    hashed_password=pwd_context.hash(create_user_request.password),
    is_active=True
  )
  return create_user_model
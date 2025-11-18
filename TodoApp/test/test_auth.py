from fastapi import HTTPException
from jose import jwt, JWTError
from datetime import timedelta
from ..routers.auth import get_db, authenticate_user, create_access_token, SECRET_KEY, ALGORITH, get_current_user
from .utils import *
import pytest


app.dependency_overrides[get_db] = override_get_db


def test_authenticate_user(test_user):
  db = TestingSessionLocal()

  authenticated_user = authenticate_user(test_user.username, 'testpassword', db)
  assert authenticated_user is not None
  assert authenticated_user.username == test_user.username # type: ignore

  no_existent_user = authenticate_user('WrongUserName', 'testpassword', db)
  assert no_existent_user is False

  wrong_password_user = authenticate_user(test_user.username, 'wrongpassword', db)
  assert wrong_password_user is False


def test_create_access_token(test_user):
  username = 'testuser'
  id = 1
  role = 'user'
  expires_delta = timedelta(days=1)

  token = create_access_token(username, id, role, expires_delta)

  decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITH], options={'verify_signature': False})

  assert decoded_token['sub'] == username
  assert decoded_token['id'] == id
  assert decoded_token['role'] == role


@pytest.mark.asyncio
async def test_get_current_user_valid_token():
  encode = {'sub': 'testuser', 'id': 1, 'role': 'admin'}
  token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITH)

  user = await get_current_user(token=token)
  assert user == {'username': 'testuser', 'id': 1, 'role': 'admin'}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
  encode = {'role': 'user'}
  token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITH)

  with pytest.raises(HTTPException) as excinfo:
    await get_current_user(token=token)
  
  assert excinfo.value.status_code == 401
  assert excinfo.value.detail == 'Could not validate user'

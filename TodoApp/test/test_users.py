from fastapi import status
from ..routers.users import get_db, get_current_user
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
  response = client.get('/user')
  assert response.status_code == status.HTTP_200_OK
  assert response.json()['username'] == 'larac' 
  assert response.json()['email'] == 'lara@gmail.com' 
  assert response.json()['first_name'] == 'Lara' 
  assert response.json()['last_name'] == 'Croft' 
  assert response.json()['role'] == 'admin'
  assert response.json()['phone_number'] == '(111)-111-1111' 



def test_change_password_success(test_user):
  response =  client.put('/user/password', json={'password': 'testpassword', 
                                                'new_password': 'newpassword'})
  assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
  response =  client.put('/user/password', json={'password': 'wrongpassword', 
                                                'new_password': 'newpassword'})
  assert response.status_code == status.HTTP_401_UNAUTHORIZED
  assert response.json() == {'detail': 'Current password is incorrect'}


def test_change_phone_number_success(test_user):
  response =  client.put('/user/phonenumber/2222222222')
  assert response.status_code == status.HTTP_204_NO_CONTENT
  
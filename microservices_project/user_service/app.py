# ==============================================================
# SISTEMAS DISTRIBUÍDOS E SOA – EXEMPLO PRÁTICO COM FASTAPI
# --------------------------------------------------------------
# Este serviço representa o lado "Servidor" em uma arquitetura
# Cliente-Servidor. Ele oferece funcionalidades (serviços) que
# podem ser invocados remotamente, como no conceito de RPC.
# ==============================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json, os

# --------------------------------------------------------------
# FastAPI cria uma interface HTTP para comunicação remota.
# Aqui o app é como um "servidor RMI" — ele disponibiliza métodos
# que podem ser chamados de forma remota por outro serviço.
# --------------------------------------------------------------
app = FastAPI(
  title="User service", 
  description="Serviço de cadastro de usuário", 
  version="1.0"
)

DATA_FILE = "users.json"

# --------------------------------------------------------------
# O arquivo JSON representa o "recurso compartilhado" entre
# processos distribuídos. Em um sistema real, isso seria um BD.
# --------------------------------------------------------------
if not os.path.exists(DATA_FILE):
  with open(DATA_FILE, 'w') as f:
    json.dump([],f)

# --------------------------------------------------------------
# Modelo de dados (equivalente a um tipo estruturado no RPC)
# --------------------------------------------------------------
class User(BaseModel):
  name: str
  email:str

# --------------------------------------------------------------
# Endpoint remoto: POST /register
# Atua como um "método remoto" (RMI) que o cliente pode invocar
# para cadastrar um usuário. Isso simula uma invocação remota.
# --------------------------------------------------------------
@app.post("/register")
def register_user(user: User):
  try:
    # Load users safely
    with open(DATA_FILE,'r+') as f:
      try:
        users = json.load(f)
      except json.JSONDecodeError:
        users = []

      # # Check if user already exists
      if any(u['email'] == user.email for u in users):
        raise HTTPException(status_code=400, detail="User already exists")
      
      # Append new user correctly
      users.append(user.model_dump())
      f.seek(0)
      json.dump(users, f, indent=2)
      f.truncate()
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Internal error: {e}")
  
  return {"message": f"User {user.name} registered successfully!"}


# --------------------------------------------------------------
# Endpoint remoto: GET /users
# Fornece a lista de usuários — outro "serviço remoto" disponível.
# --------------------------------------------------------------
@app.get("/users")
def list_users():
  try:
    with open(DATA_FILE, "r") as f:
      try:
        users = json.load(f)
      except json.JSONDecodeError:
        raise HTTPException(status_code=404, detail=f"Users not founds.") 
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Internal error: {e}")
  return users
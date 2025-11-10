# ==============================================================
# SISTEMAS DISTRIBUÍDOS E SOA – EXEMPLO PRÁTICO COM FASTAPI
# --------------------------------------------------------------
# Este serviço representa o lado "Cliente" na arquitetura
# Cliente-Servidor. Ele realiza chamadas remotas (RPC/REST)
# para o User Service, simulando comunicação distribuída.
# ==============================================================

from fastapi import FastAPI, HTTPException
import json, os, requests

app = FastAPI(title="Query Service", description="Serviço de consulta de usuário", version="1.0")

DATA_FILE = "../user_service/users.json"


# --------------------------------------------------------------
# Endpoint: /find
# Esse endpoint faz uma consulta local (simulando uma cópia do
# banco de dados ou cache local em um sistema distribuído).
# --------------------------------------------------------------
@app.get("/find")
def find_user(email:str):
  if not os.path.exists(DATA_FILE):
    raise HTTPException(status_code=500, detail="Database not found.")
  
  try:
    with open(DATA_FILE, 'r') as f:
      try:
        users = json.load(f)

        for user in users:
          if user["email"] == email:
            return user

        raise HTTPException(status_code=404, detail="User not found")
      except json.JSONDecodeError:
        raise HTTPException(status_code=404, detail=f"Database empty.")
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Internal error: {e}")


# --------------------------------------------------------------
# Endpoint: /remote-list
# Este é o ponto mais importante — simula uma chamada RPC.
#
# resp = requests.get("http://user_service:5000/users")
#
# Aqui, o Query Service faz uma CHAMADA REMOTA ao User Service.
# → Isso representa uma "Remote Procedure Call (RPC)"
#   feita sobre HTTP (RESTful RPC).
#
# Também é um exemplo de "comunicação síncrona":
# o cliente espera a resposta antes de continuar a execução.
# --------------------------------------------------------------
@app.get("/remote-list")
def get_remote_list():
  try:
    resp = requests.get("http://localhost:5000/users")
    return resp.json()
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
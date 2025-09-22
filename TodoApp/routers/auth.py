from fastapi import FastAPI, APIRouter

router = APIRouter()

@router.get("/auth/")
async def get_user():
  return {'user': 'authenticated'}
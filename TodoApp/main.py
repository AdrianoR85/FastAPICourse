from fastapi import FastAPI
from database import engine
import models


app = FastAPI()

print(models.Base.metadata.tables)
models.Base.metadata.create_all(bind=engine)
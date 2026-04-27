from fastapi import FastAPI, Depends
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session

Base.metadata.create_all(engine)

app = FastAPI(title="Global Education API")

@app.get("/")
def root():
    return {"message": "Global Education API is running"}
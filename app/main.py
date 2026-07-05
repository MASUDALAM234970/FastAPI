from fastapi import FastAPI , Depends
from pydantic import BaseModel, HttpUrl
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from typing import Optional
from . import models
from sqlalchemy.orm import session
from . database import engine ,get_db


app =FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/api/")
def course(db:session =Depends(get_db)):
    return{"status":"sqlalchemy ORM working"}
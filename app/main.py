from fastapi import FastAPI, Depends
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


class CourseCreate(BaseModel):
    name: str
    instructor: str
    duration: float
    price: float
    website: HttpUrl


@app.post("/api")
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db)
):
    new_course = models.Course(
        name=course.name,
        instructor=course.instructor,
        duration=course.duration,
        price=course.price,
        website=str(course.website)
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course

@app.get("/api")
def course(db:Session =Depends(get_db)):
    course=db.query(models.Course).all()
    return course
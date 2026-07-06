from fastapi import FastAPI, Depends
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from typing import Optional

from . import models
from .database import engine, get_db

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


class CourseCreate(BaseModel):
    name: Optional[str] = None
    instructor: Optional[str] = None
    duration: Optional[float] = None
    price: Optional[float] = None
    website: Optional[HttpUrl] = None


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

@app.put("/api/{id}")
def update_course(
    id: int,
    course: CourseCreate,
    db: Session = Depends(get_db)
):
    db_course = db.query(models.Course).filter(
        models.Course.id == id
    ).first()

    if not db_course:
        return {"message": "Course not found"}

    db_course.name = course.name
    db_course.instructor = course.instructor
    db_course.duration = course.duration
    db_course.price = course.price
    db_course.website = str(course.website)

    db.commit()
    db.refresh(db_course)

    return db_course

@app.patch("/api/{id}")
def patch_course(
    id: int,
    course: CourseCreate,
    db: Session = Depends(get_db)
):
    db_course = db.query(models.Course).filter(
        models.Course.id == id
    ).first()

    if not db_course:
        return {"message": "Course not found"}

    if course.name is not None:
        db_course.name = course.name

    if course.instructor is not None:
        db_course.instructor = course.instructor

    if course.duration is not None:
        db_course.duration = course.duration

    if course.price is not None:
        db_course.price = course.price

    if course.website is not None:
        db_course.website = str(course.website)

    db.commit()
    db.refresh(db_course)

    return db_course

@app.delete("/api/{id}")
def delete_course(
    id: int,
    db: Session = Depends(get_db)
):
    db_course = db.query(models.Course).filter(
        models.Course.id == id
    ).first()

    if not db_course:
        return {"message": "Course not found"}

    db.delete(db_course)
    db.commit()

    return {"message": "Course deleted successfully"}

@app.get("/api/{id}")
def get_course(
    id: int,
    db: Session = Depends(get_db)
):
    course = db.query(models.Course).filter(
        models.Course.id == id
    ).first()

    if not course:
        return {"message": "Course not found"}

    return course
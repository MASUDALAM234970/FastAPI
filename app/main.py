from fastapi import FastAPI, Depends

from sqlalchemy.orm import Session


from fastapi import HTTPException

from . import models,schemas
from .database import engine, get_db

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.post("/api", response_model=schemas.CourseResponse)
def create_course(
    course: schemas.CourseCreate,
    db: Session = Depends(get_db)
):
    new_course = models.Course(**course.model_dump())

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course

@app.get("/api", response_model=list[schemas.CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(models.Course).all()
    return courses


@app.get("/api/{id}", response_model=schemas.CourseResponse)
def get_course(id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(
        models.Course.id == id
    ).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return course

@app.put("/api/{id}", response_model=schemas.CourseResponse)
def update_course(
    id: int,
    course: schemas.CourseCreate,
    db: Session = Depends(get_db)
):
    existing_course = db.query(models.Course).filter(
        models.Course.id == id
    ).first()

    if not existing_course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    existing_course.name = course.name
    existing_course.instructor = course.instructor
    existing_course.duration = course.duration

    db.commit()
    db.refresh(existing_course)

    return existing_course

@app.patch("/api/{id}", response_model=schemas.CourseResponse)
def patch_course(
    id: int,
    course: schemas.CourseCreate,
    db: Session = Depends(get_db)
):
    existing_course = db.query(models.Course).filter(
        models.Course.id == id
    ).first()

    if not existing_course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    update_data = course.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(existing_course, key, value)

    db.commit()
    db.refresh(existing_course)

    return existing_course

@app.delete("/api/{id}")
def delete_course(
    id: int,
    db: Session = Depends(get_db)
):
    course = db.query(models.Course).filter(
        models.Course.id == id
    ).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    db.delete(course)
    db.commit()

    return {
        "message": "Course deleted successfully"
    }
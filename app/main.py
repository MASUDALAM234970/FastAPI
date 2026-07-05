from fastapi import FastAPI ,HTTPException ,status
from pydantic import BaseModel, HttpUrl
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from typing import Optional

app =FastAPI()

# class Course(BaseModel):
#     name: str
#     instructor: str
#     duration: int
#     website: HttpUrl
             
    
class Course(BaseModel):
    name: Optional[str] = None
    instructor: Optional[str] = None
    duration: Optional[int] = None
    website: Optional[HttpUrl] = None 
        



while True:
   try: 
       conn = psycopg2.connect(host='localhost',database="alam",user="postgres",password='234970', cursor_factory=RealDictCursor)
       cursor=conn.cursor()
       print("Successfully connected Database")
       break
   except Exception as error:
       print("Database connection failed ")
       print("Error:",error) 
       time.sleep(2)


@app.get("/api/")
def alam():
    cursor.execute("SELECT * FROM course")
    data = cursor.fetchall()
    return {"data": data}

@app.post("/api/post")
def create_course(course: Course):
    cursor.execute(
        """
        INSERT INTO course (name, instructor, duration, website)
        VALUES (%s, %s, %s, %s)
        """,
        (
            course.name,
            course.instructor,
            course.duration,
            str(course.website)
        )
    )
    conn.commit()

    return {"message": "Course created successfully"}

@app.get("/api/{id}")
def get_course(id: int):
    cursor.execute(
        "SELECT * FROM course WHERE id = %s",
        (id,)
    )

    course = cursor.fetchone()

    return {"data": course}


from fastapi import HTTPException, status

@app.delete("/api/{id}", status_code=status.HTTP_200_OK)
def delete_course(id: int):
    cursor.execute(
        "DELETE FROM course WHERE id = %s RETURNING *",
        (id,)
    )

    deleted_course = cursor.fetchone()
    conn.commit()

    if deleted_course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    return {
        "message": "Course deleted successfully"
    }


@app.put("/api/{id}")
def update_course(id: int, course: Course):

    cursor.execute(
        """
        UPDATE course
        SET name = %s,
            instructor = %s,
            duration = %s,
            website = %s
        WHERE id = %s
        RETURNING *
        """,
        (
            course.name,
            course.instructor,
            course.duration,
            str(course.website),
            id
        )
    )

    updated_course = cursor.fetchone()
    conn.commit()

    if updated_course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return {
        "message": "Course updated successfully",
        "data": updated_course
    }

from fastapi import HTTPException

@app.patch("/api/{id}")
def update_course(id: int, course: Course):

    update_data = course.model_dump(exclude_unset=True)

    if not update_data:
        return {"message": "No fields provided"}

    query = "UPDATE course SET "
    values = []

    for key, value in update_data.items():
        query += f"{key} = %s, "
        values.append(str(value) if key == "website" else value)

    query = query.rstrip(", ")
    query += " WHERE id = %s RETURNING *"

    values.append(id)

    cursor.execute(query, tuple(values))

    updated_course = cursor.fetchone()
    conn.commit()

    if updated_course is None:
        return {"message": "Course not found"}

    return {
        "message": "Course updated successfully",
        "data": updated_course
    }
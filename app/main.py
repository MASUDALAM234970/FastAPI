from fastapi import FastAPI 
from pydantic import BaseModel, HttpUrl
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app =FastAPI()

class Course(BaseModel):
    name: str
    instructor: str
    duration: int
    website: HttpUrl
             
    
          
        



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
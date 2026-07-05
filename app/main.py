from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app =FastAPI()


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
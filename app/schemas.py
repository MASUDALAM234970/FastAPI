from pydantic import BaseModel ,EmailStr
from typing import Optional
from datetime import datetime
class CourseCreate(BaseModel):
    name: Optional[str] = None
    instructor: Optional[str] = None
    duration: Optional[float] = None
    price: Optional[float] = None
    website: Optional[str] = None
class CourseResponse(CourseCreate):
    id : int

    class Config:
        orm_model =True

class UserCrete(BaseModel):
    email : EmailStr
    password :str    

class UserRes(BaseModel):
    
    id : int 
    email :EmailStr
    created_at : datetime
    
    class Config:
        orrm_model =True
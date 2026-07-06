from pydantic import BaseModel 
from typing import Optional
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
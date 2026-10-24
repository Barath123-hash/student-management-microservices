from pydantic import BaseModel, Field
from typing import Optional


class CourseCreate(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=5)
    duration: str = Field(min_length=2, max_length=50)
    instructor: str = Field(min_length=2, max_length=100)


class CourseUpdate(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=5)
    duration: str = Field(min_length=2, max_length=50)
    instructor: str = Field(min_length=2, max_length=100)


class CourseResponse(BaseModel):
    id: int
    title: str
    description: str
    duration: str
    instructor: str

    class Config:
        from_attributes = True

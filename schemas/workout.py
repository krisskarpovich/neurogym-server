from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class WorkoutBaseSchema(BaseModel):
    exercise_type: str
    logo_url: Optional[str] = None
    instructions: Optional[str] = None
    image_url: Optional[str] = None


class WorkoutCreateSchema(WorkoutBaseSchema):
    pass



class WorkoutTypeSchema(BaseModel):
    id: int
    exercise_type: str
    logo_url: str | None = None

    class Config:
        orm_mode = True


class WorkoutSchema(BaseModel):
    id: int
    workout_title: str
    logo_url: Optional[str] = None
    instructions: Optional[str] = None
    image_url: Optional[str] = None
    workout_type: WorkoutTypeSchema  # Вложенный объект
    

    class Config:
        orm_mode = True
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


class WorkoutSchema(WorkoutBaseSchema):
    id: int

    class Config:
        orm_mode = True

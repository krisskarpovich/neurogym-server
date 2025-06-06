
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime


class WorkoutResultCreate(BaseModel):
    workout_id: int
    date: datetime
    duration_minutes: Optional[int] = None
    sets: Optional[int] = None
    reps: Optional[int] = None
    calories_burned: Optional[float] = None
    tips: Optional[str] = None
    completion: Optional[float] = None
    
    class Config:
        orm_mode = True

class WorkoutResultRead(WorkoutResultCreate):
    id: int 
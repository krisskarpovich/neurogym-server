from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserWorkoutBase(BaseModel):
    user_id: int
    workout_id: int
    video_url: Optional[str] = None
    workout_date: Optional[datetime] = None


class UserWorkoutCreate(UserWorkoutBase):
    pass


class UserWorkout(UserWorkoutBase):
    class Config:
        orm_mode = True

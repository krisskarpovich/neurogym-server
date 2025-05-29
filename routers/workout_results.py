from fastapi import APIRouter, Depends, FastAPI, Form, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import Date, cast, select
from database import get_db

from sqlalchemy.orm import Session

from models.workout import User, WorkoutResult
from schemas.workout_result import WorkoutResultCreate, WorkoutResultRead
from services.get_user import get_current_user_from_token

router = APIRouter()


@router.post("/", response_model=WorkoutResultRead)
def save_workout_result(
    result: WorkoutResultCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    try:
        duration = result.duration_minutes or 0
        sets = result.sets or 0
        reps = result.reps or 0

        calculated_calories = (duration * 5) + (sets * reps * 0.1)

        db_result = WorkoutResult(
            **result.dict(exclude={"calories_burned"}),
            calories_burned=calculated_calories,
            user_id=current_user.id,
        )

        db.add(db_result)
        db.commit()
        db.refresh(db_result)
        return db_result
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date, datetime


@router.get("/by_date", response_model=List[WorkoutResultRead])
def get_workouts_by_date(
    workout_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    start = datetime.combine(workout_date, datetime.min.time())
    end = datetime.combine(workout_date, datetime.max.time())

    results = (
        db.query(WorkoutResult)
        .filter(
            WorkoutResult.user_id == current_user.id,
            WorkoutResult.date >= start,
            WorkoutResult.date <= end,
        )
        .all()
    )
    return results

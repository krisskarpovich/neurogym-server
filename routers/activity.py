from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, datetime
from sqlalchemy import func
from database import get_db
from models.workout import User, WorkoutResult
from schemas.daily_activity import DailyActivitySummary
from services.get_user import get_current_user_from_token

router = APIRouter()


# @router.get("/by_date", response_model=DailyActivitySummary)
# def get_daily_activity_summary(
#     user_id: int, workout_date: date, db: Session = Depends(get_db)
# ):
#     start = datetime.combine(workout_date, datetime.min.time())
#     end = datetime.combine(workout_date, datetime.max.time())

#     summary = (
#         db.query(
#             func.count(WorkoutResult.id).label("workout_count"),
#             func.sum(WorkoutResult.calories).label("total_calories"),
#             func.sum(WorkoutResult.duration_minutes).label("total_minutes"),
#         )
#         .filter(
#             WorkoutResult.user_id == user_id,
#             WorkoutResult.date >= start,
#             WorkoutResult.date <= end,
#         )
#         .first()
#     )

#     return DailyActivitySummary(
#         workout_count=summary.workout_count or 0,
#         total_calories=summary.total_calories or 0,
#         total_minutes=summary.total_minutes or 0,
#     )



@router.get("/by_date", response_model=DailyActivitySummary)
def get_daily_activity_summary(
    workout_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    start = datetime.combine(workout_date, datetime.min.time())
    end = datetime.combine(workout_date, datetime.max.time())

    summary = (
        db.query(
            func.count(WorkoutResult.id).label("workout_count"),
            func.sum(WorkoutResult.calories_burned).label("total_calories"),
            func.sum(WorkoutResult.duration_minutes).label("total_minutes"),
        )
        .filter(
            WorkoutResult.user_id == current_user.id,
            WorkoutResult.date >= start,
            WorkoutResult.date <= end,
        )
        .first()
    )

    return DailyActivitySummary(
        workout_count=summary.workout_count or 0,
        total_calories=summary.total_calories or 0,
        total_minutes=summary.total_minutes or 0,
    )

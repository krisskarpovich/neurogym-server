from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import APIRouter, Depends
from datetime import datetime, timedelta

from typing import List

from database import get_db
from models.workout import User, WorkoutResult
from services.get_user import get_current_user_from_token

router = APIRouter()


@router.get("/weekly", summary="Get weekly completion stats")
def get_weekly_statistics(
    current_user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db),
):
    today = datetime.utcnow().date()
    seven_days_ago = today - timedelta(days=8)

    results = (
        db.query(
            func.date(WorkoutResult.date).label("day"),
            func.avg(WorkoutResult.completion).label("avg_completion"),
            func.sum(WorkoutResult.calories_burned).label("total_calories"),
            func.sum(WorkoutResult.duration_minutes).label("total_minutes"),
        )
        .filter(
            WorkoutResult.user_id == current_user.id,
            WorkoutResult.date >= seven_days_ago,
            WorkoutResult.date <= today,
        )
        .group_by(func.date(WorkoutResult.date))
        .order_by(func.date(WorkoutResult.date))
        .all()
    )

    return [
        {
            "date": r.day,  
            "avg_completion": round(r.avg_completion or 0, 2),
            "total_calories": int(r.total_calories or 0),
            "total_minutes": int(r.total_minutes or 0),
        }
        for r in results
    ]

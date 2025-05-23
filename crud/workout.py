from sqlalchemy.orm import Session
from models.workout import Workout
from schemas.workout import WorkoutCreate

def create_workout(db: Session, user_id: int, workout_data: WorkoutCreate):
    workout = Workout(
        user_id=user_id,
        exercise_type=workout_data.exercise_type,
        calories=workout_data.calories,
        duration_minutes=workout_data.duration_minutes,
    )
    db.add(workout)
    db.commit()
    db.refresh(workout)
    return workout

# def get_user_workouts(db: Session, user_id: int):
#     return db.query(Workout).filter(Workout.user_id == user_id).order_by(Workout.date.desc()).all()

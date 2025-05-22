from sqlalchemy.orm import Session
from models.workout import UserWorkout

from schemas.user_workout import UserWorkoutCreate


def create_user_workout(db: Session, user_workout: UserWorkoutCreate):
    db_user_workout = UserWorkout(**user_workout.dict())  # Создаем объект тренировки пользователя
    db.add(db_user_workout)
    db.commit()
    db.refresh(db_user_workout)
    return db_user_workout

def get_user_workouts(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(UserWorkout).filter(UserWorkout.user_id == user_id).offset(skip).limit(limit).all()

def get_user_workout_by_id(db: Session, user_id: int, workout_id: int):
    return db.query(UserWorkout).filter(UserWorkout.user_id == user_id, UserWorkout.workout_id == workout_id).first()

def update_user_workout(db: Session, user_workout_id: int, user_workout: UserWorkoutCreate):
    db_user_workout = db.query(UserWorkout).filter(UserWorkout.id == user_workout_id).first()
    if db_user_workout:
        for key, value in user_workout.dict().items():
            setattr(db_user_workout, key, value)
        db.commit()
        db.refresh(db_user_workout)
    return db_user_workout

def delete_user_workout(db: Session, user_workout_id: int):
    db_user_workout = db.query(UserWorkout).filter(UserWorkout.id == user_workout_id).first()
    if db_user_workout:
        db.delete(db_user_workout)
        db.commit()
    return db_user_workout

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.workout import Workout
from models.workout import User
from schemas.workout import WorkoutCreateSchema

def create_workout(db: Session, workout: WorkoutCreateSchema):
    db_workout = Workout(**workout.dict())  
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout) 
    return db_workout


def get_workouts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Workout).offset(skip).limit(limit).all()


def get_workout_by_id(db: Session, workout_id: int):
    return db.query(Workout).filter(Workout.id == workout_id).first()






def get_workout_by_id(db: Session, workout_id: int) -> Workout | None:
    return db.query(Workout).filter(Workout.id == workout_id).first()


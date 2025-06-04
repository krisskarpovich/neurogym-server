from typing import List
from fastapi import APIRouter, FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from services.workout import create_workout, get_workout_by_id, get_workouts
from schemas.workout import WorkoutSchema, WorkoutCreateSchema, WorkoutTypeSchema
from models.workout import Workout, WorkoutType

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=WorkoutSchema)
def create_workout_endpoint(workout: WorkoutCreateSchema, db: Session = Depends(get_db)):
    return create_workout(db=db, workout=workout)

# @router.get("/", response_model=list[WorkoutSchema])
# def read_workouts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     return get_workouts(db=db, skip=skip, limit=limit)


# с типом

@router.get("/types", response_model=List[WorkoutTypeSchema])
def get_workout_types(db: Session = Depends(get_db)):
    return db.query(WorkoutType).all()

@router.get("/by_type/{type_id}", response_model=List[WorkoutSchema])
def get_workouts_by_type(type_id: int, db: Session = Depends(get_db)):
    workouts = db.query(Workout).filter(Workout.workout_type_id == type_id).all()
    return workouts

@router.get("/{workout_id}", response_model=WorkoutSchema)
def read_workout_by_id(workout_id: int, db: Session = Depends(get_db)):
    workout = get_workout_by_id(db, workout_id)
    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout
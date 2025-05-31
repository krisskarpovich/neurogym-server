from sqlalchemy import (
    ARRAY,
    JSON,
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey,
    DateTime,
    Text,
)
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class ExerciseTip(Base):
    __tablename__ = "exercise_tips"

    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False)
    condition_key = Column(String, nullable=False)  
    condition_operator = Column(String, nullable=False) 
    condition_value = Column(String, nullable=False) 
    message = Column(Text, nullable=False)

    workout = relationship("Workout", back_populates="tips")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True)
    token = Column(String, unique=True)
    user_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    weight = Column(Float)
    height = Column(Float)
    birth_date = Column(Date)

    workout_results = relationship(
        "WorkoutResult", back_populates="user"
    )  

# class Workout(Base):
#     __tablename__ = "workouts"

#     id = Column(Integer, primary_key=True, index=True)
#     logo_url = Column(String, nullable=True)
#     exercise_type = Column(String, nullable=False)
#     instructions = Column(String)
#     image_url = Column(String, nullable=True)

#     tips = relationship("ExerciseTip", back_populates="workout")

class WorkoutType(Base):
    __tablename__ = "workout_types"

    id = Column(Integer, primary_key=True, index=True)
    exercise_type = Column(String, nullable=False)
    logo_url = Column(String, nullable=True)

    workouts = relationship("Workout", back_populates="workout_type")

# class Workout(Base):
#     __tablename__ = "workouts"

#     id = Column(Integer, primary_key=True, index=True)
#     workout_type_id = Column(Integer, ForeignKey("workout_types.id"), nullable=False)

#     instructions = Column(String)
#     image_url = Column(String, nullable=True)

#     workout_type = relationship("WorkoutType", back_populates="workouts")

#     tips = relationship("ExerciseTip", back_populates="workout")

class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    workout_type_id = Column(Integer, ForeignKey("workout_types.id"), nullable=False)

    workout_title = Column(String, nullable=False)
    logo_url = Column(String, nullable=True)      
    instructions = Column(String)
    image_url = Column(String, nullable=True)

    workout_type = relationship("WorkoutType", back_populates="workouts")
    tips = relationship("ExerciseTip", back_populates="workout")


class WorkoutResult(Base):
    __tablename__ = "workout_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    workout_id = Column(Integer)
    date = Column(DateTime, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    sets = Column(Integer, nullable=True)
    reps = Column(Integer, nullable=True)
    calories_burned = Column(Float, nullable=True)
    tips = Column(String, nullable=True)
    completion = Column(Float, nullable=True)

    user = relationship("User", back_populates="workout_results")

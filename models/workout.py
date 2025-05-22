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

# from sqlalchemy import Column, Integer, String, ForeignKey, Text
# from sqlalchemy.orm import relationship
# from database import Base


class ExerciseTip(Base):
    __tablename__ = "exercise_tips"

    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False)
    condition_key = Column(String, nullable=False)  # Например: "avg_knee_angle"
    condition_operator = Column(String, nullable=False)  # Например: "<", ">", "=="
    condition_value = Column(String, nullable=False)  # Значение для сравнения
    message = Column(Text, nullable=False)

    workout = relationship("Workout", back_populates="tips")


# class Token(Base):
#     __tablename__ = "tokens"

#     id = Column(Integer, primary_key=True, index=True)
#     access_token = Column(String, unique=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     created_at = Column(DateTime, default=datetime.utcnow)
#     expires_at = Column(DateTime)

#     user = relationship("User", back_populates="tokens")


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

    user_workouts = relationship("UserWorkout", back_populates="user")

    workout_results = relationship(
        "WorkoutResult", back_populates="user"
    )  # вот это нужно


# Модель тренировки (Workout)
class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    logo_url = Column(String, nullable=True)
    exercise_type = Column(String, nullable=False)
    instructions = Column(String)
    image_url = Column(String, nullable=True)

    user_workouts = relationship("UserWorkout", back_populates="workout")
    tips = relationship("ExerciseTip", back_populates="workout")


class UserWorkout(Base):
    __tablename__ = "user_workouts"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"), primary_key=True)
    video_url = Column(String, nullable=True)
    workout_date = Column(DateTime, default=datetime.utcnow)  # Дата тренировки

    user = relationship("User", back_populates="user_workouts")

    workout = relationship("Workout", back_populates="user_workouts")

    # models/workout_result.py


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

    user = relationship("User", back_populates="workout_results")

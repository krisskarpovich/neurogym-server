from sqlalchemy.orm import Session
from models.workout import User
from schemas.user import UserCreate
import math

def create_user(db: Session, user: UserCreate):
    bmi = user.weight * math.pow(user.height * 100, 2)
    db_user = User(
        email=user.email,
        password=user.password,  # пока без хеширования
        first_name=user.first_name,
        birth_date=user.birth_date,
        weight=user.weight,
        height=user.height,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from schemas.user import TokenResponse, UserCreate, UserLogin, UserResponse
from models.workout import RefreshToken, User
from database import get_db
from services.auth_service import hash_password, verify_password
from services.get_user import get_current_user_from_token
from utils.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
    save_refresh_token,
)

router = APIRouter()

from jose import JWTError
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session


from fastapi.responses import JSONResponse


@router.post("/register", response_model=TokenResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user_data.password)

    new_user = User(
        email=user_data.email,
        hashed_password=hashed_pw,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        weight=user_data.weight,
        height=user_data.height,
        birth_date=user_data.birth_date,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": str(new_user.id)})
    save_refresh_token(db, new_user.id, token)

    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=TokenResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    print("Received token:", "authorization")

    # Сохраняем refresh токен в БД
    save_refresh_token(db, user.id, refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


from fastapi import Body


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(refresh_token: str = Body(...), db: Session = Depends(get_db)):
    try:
        payload = decode_token(refresh_token)
        user_id = int(payload.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Проверяем, есть ли этот refresh токен в базе
    db_token = (
        db.query(RefreshToken).filter_by(token=refresh_token, user_id=user_id).first()
    )
    if not db_token:
        raise HTTPException(status_code=401, detail="Refresh token not found")

    new_access_token = create_access_token({"sub": str(user_id)})
    new_refresh_token = create_refresh_token({"sub": str(user_id)})

    # Обновляем refresh token в базе
    db_token.token = new_refresh_token
    db.commit()

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }


from fastapi import Header


@router.get("/me", response_model=UserResponse)
def get_current_user(
    current_user: User = Depends(get_current_user_from_token),
    authorization: str = Header(None),
):
    print("Received token:", authorization)

    bmi = 0
    if current_user.weight and current_user.height:
        bmi = current_user.weight / (current_user.height**2)

    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        bmi=bmi,
    )


@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_db)):
    db.query(RefreshToken).filter(RefreshToken.token == refresh_token).delete()
    db.commit()
    return {"message": "Logged out"}

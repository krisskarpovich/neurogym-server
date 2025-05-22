from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from jose import jwt
from datetime import datetime, timedelta

from models.workout import RefreshToken

SECRET = "super-secret"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_minutes=100):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)

def create_refresh_token(data: dict, expires_days=7):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=expires_days)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)

def decode_token(token: str):
    return jwt.decode(token, SECRET, algorithms=[ALGORITHM])

def save_refresh_token(db: Session, user_id: int, token: str):
    new_refresh = RefreshToken(user_id=user_id, token=token)
    db.add(new_refresh)
    db.commit()


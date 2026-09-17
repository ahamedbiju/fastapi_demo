from datetime import datetime, timedelta, UTC
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from db_models import User as DBUser



SECRET_KEY = "change_this_later_to_env_variable"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(401, "Invalid token")

        user = (
            db.query(DBUser)
            .filter(DBUser.id == int(user_id))
            .first()
        )

        if user is None:
            raise HTTPException(401, "Invalid token")

        return user

    except JWTError:
        raise HTTPException(401, "Invalid token")
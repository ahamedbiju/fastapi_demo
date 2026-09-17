from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from db_models import User as DBUser
from security import verify_password
from auth import create_access_token


router = APIRouter(tags=["Authentication"])



@router.post("/login")
def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = (
        db.query(DBUser)
        .filter(DBUser.name == credentials.username)
        .first()
    )

    if user is None:
        raise HTTPException(401, "Invalid credentials")

    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token({"sub": str(user.id)})

    return {"access_token": token, "token_type": "bearer"}

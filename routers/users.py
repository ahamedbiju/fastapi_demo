from fastapi import APIRouter, Depends ,HTTPException
from sqlalchemy.orm import Session

from database import get_db
from db_models import User as DBUser
from models import UserCreate, User, UserWithProducts 
from security import hash_password
from auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = DBUser(name=user.name,
                      hashed_password=hash_password(user.password))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/", response_model=list[User])
def get_users(db: Session = Depends(get_db)):
    return db.query(DBUser).all()

@router.get("/me", response_model=User)
def me(current_user: DBUser = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=UserWithProducts)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = (
        db.query(DBUser)
        .filter(DBUser.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(404, "User not found")

    return user

@router.get("/{user_id}/products")
def get_user_products(user_id: int, db: Session = Depends(get_db)):
    user = (
        db.query(DBUser)
        .filter(DBUser.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(404, "User not found")

    return user.products


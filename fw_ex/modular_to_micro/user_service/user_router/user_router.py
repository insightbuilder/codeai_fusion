from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from services.user_service import register_user, authenticate_user
from pydantic import BaseModel

router = APIRouter()


class UserRequest(BaseModel):
    username: str
    password: str


@router.post("/register")
def register(user_data: UserRequest, db: Session = Depends(get_db)):
    return register_user(db, user_data.username, user_data.password)


@router.post("/token")
def login(user_data: UserRequest, db: Session = Depends(get_db)):
    return authenticate_user(db, user_data.username, user_data.password)

from fastapi import APIRouter, HTTPException, Depends
from core.auth import create_access_token, verify_password
from repositories.user_repository import get_user_by_username
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from core.database import get_db

router = APIRouter()


@router.post("/token")
def login(username: str, password: str, db: Session = Depends(get_db)):
    # Get user from the database by username
    user = get_user_by_username(db=db, username=username)

    if user is None or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create and return JWT token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

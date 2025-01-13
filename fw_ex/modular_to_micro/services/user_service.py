from repositories.user_repository import create_user, get_user_by_username
from core.auth import hash_password, verify_password, create_access_token
from sqlalchemy.orm import Session
from fastapi import HTTPException


def register_user(db: Session, username: str, password: str):
    """
    Registers a new user after hashing the password.
    """
    if get_user_by_username(db, username):
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = hash_password(password)
    user = create_user(db, username, hashed_pw)
    return {"id": user.id, "username": user.username}


def authenticate_user(db: Session, username: str, password: str):
    """
    Authenticates a user and returns a JWT token.
    """
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return create_access_token({"sub": user.username})

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    age: int = Field(..., ge=18, le=100)


@app.post("/validate/")
async def validate_user(user: User):
    return {"message": f"User {user.username} is valid"}

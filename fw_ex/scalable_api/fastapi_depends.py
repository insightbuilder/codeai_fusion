from fastapi import Depends, FastAPI
from typing import Annotated
from inject_deps import DatabaseService

app = FastAPI()


def get_db():
    return DatabaseService()


@app.get("/users")
async def read_users(db: Annotated[DatabaseService, Depends(get_db)]):
    return {"db": db.connect()}

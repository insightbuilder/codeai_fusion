from personmodel import Person
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, create_engine, Session, select
from typing import Annotated

# pyright: reportReturnType=false
db = "person.db"
url = f"sqlite:///{db}"

engine = create_engine(url, connect_args={"check_same_thread": False})


def get_per_session():
    with Session(engine) as sess:
        yield sess


SessionDepPer = Annotated[Session, Depends(get_per_session)]

app = FastAPI()


@app.get("/person")
async def root():
    return {"person": "hello from person server"}


@app.post("/person/add")
async def add_persons(
    session: SessionDepPer,
    person: Person,
) -> Person:
    session.add(person)
    session.commit()
    session.refresh(person)
    return person


@app.get("/person/all")
async def list_persons(
    session: SessionDepPer, offset: int = 0, limit: int = 5
) -> list[Person]:
    persons = session.exec(select(Person).offset(offset).limit(limit)).all()
    return persons


@app.get("/person/{pid}")
async def get_person(session: SessionDepPer, pid: int) -> Person:
    person = session.get(Person, pid)
    if not person:
        raise HTTPException(status_code=404, detail="Person missing")
    return person


@app.delete("/person/{pid}")
async def del_person(session: SessionDepPer, pid: int):
    person = session.get(Person, pid)
    if not person:
        raise HTTPException(status_code=404, detail="Person Missing")
    session.delete(person)
    session.commit()
    return {"ok": True}

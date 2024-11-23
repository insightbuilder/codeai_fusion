from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Annotated


class Person(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int = Field(default=1)
    location: str = Field(index=True)


db = "person.db"
url = f"sqlite:///{db}"
engine = create_engine(url, connect_args={"check_same_thread": False})


def create_schema():
    SQLModel.metadata.create_all(engine)


create_schema()

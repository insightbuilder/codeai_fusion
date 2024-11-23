from fastapi import Depends
from sqlmodel import SQLModel, Field, create_engine, Session, Field, table
from typing import Annotated

# pyright: reportGeneralTypeIssues=false


class Person(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(index=True)
    location: str = Field(default=None)


sql_db = "person.db"
sql_link = f"sqlite:///{sql_db}"

connect_args = {"check_same_thread": False}
engine = create_engine(sql_link, connect_args=connect_args)


def create_db_table():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


create_db_table()

from typing import Annotated

from fastapi import Depends

from sqlmodel import Field, Session, SQLModel, create_engine, select

# pyright: reportGeneralTypeIssues=false


class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    qty: int | None = Field(default=None, index=True)
    price: int = Field(default=10)


sqlite_file = "product.db"
sqlite_url = f"sqlite:///{sqlite_file}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


create_db_and_tables()
# SessionDep = Annotated[Session, Depends(get_session)]

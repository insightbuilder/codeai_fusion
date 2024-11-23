# pyright: reportGeneralTypeIssues=false

from fastapi import FastAPI, Depends, Query
from models import Product
from sqlmodel import create_engine, Session, select
from typing import Annotated

app = FastAPI()
pdt_url = "sqlite:///product.db"
per_url = "sqlite:///person.db"

connect_args = {"check_same_thread": False}

pdt_engine = create_engine(pdt_url, connect_args=connect_args)
per_engine = create_engine(per_url, connect_args=connect_args)


def get_pdt_session():
    with Session(pdt_engine) as pdtses:
        yield pdtses


def get_per_session():
    with Session(per_engine) as perses:
        yield perses


SessionDepPdt = Annotated[Session, Depends(get_pdt_session)]
SessionDepPer = Annotated[Session, Depends(get_per_session)]


@app.get("/")
async def root():
    return {"message": "Product Micro Services"}


@app.get("/pdts")
async def get_pdt(
    session: SessionDepPdt,
    offset: int = 0,
    limit: Annotated[int, Query(le=5)] = 5,
) -> list[Product]:
    pdts = session.exec(select(Product).offset(offset).limit(limit)).all()
    return pdts


@app.post("/pdt")
async def post_pdt(session: SessionDepPdt, pdt: Product) -> Product:
    session.add(pdt)
    session.commit()
    session.refresh(pdt)
    return pdt

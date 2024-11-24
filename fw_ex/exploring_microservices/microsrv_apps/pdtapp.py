# pyright: reportGeneralTypeIssues=false
# pyright: reportReturnType=false

from fastapi import FastAPI, Depends, Query, HTTPException
from models import Product
from sqlmodel import create_engine, Session, select
from typing import Annotated

app = FastAPI()
pdt_url = "sqlite:///product.db"

connect_args = {"check_same_thread": False}

pdt_engine = create_engine(pdt_url, connect_args=connect_args)


def get_pdt_session():
    with Session(pdt_engine) as pdtses:
        yield pdtses


SessionDepPdt = Annotated[Session, Depends(get_pdt_session)]


@app.get("/")
async def root():
    return {"message": "Product Micro Services"}


@app.get("/pdts")
async def get_pdts(
    session: SessionDepPdt,
    offset: int = 0,
    limit: Annotated[int, Query(le=5)] = 50,
) -> list[Product]:
    pdts = session.exec(select(Product).offset(offset).limit(limit)).all()
    return pdts


@app.get("/pdt/{pdt_id}")
async def get_pdt(session: SessionDepPdt, pdt_id: int) -> Product:
    pdt1 = session.get(Product, pdt_id)
    if not pdt1:
        raise HTTPException(status_code=404, detail="Product not present")
    return pdt1


@app.post("/pdt")
async def post_pdt(session: SessionDepPdt, pdt: Product) -> Product:
    print(pdt)
    session.add(pdt)
    session.commit()
    session.refresh(pdt)
    return pdt


@app.delete("/pdtdel/{pdt_id}")
async def del_pdt(session: SessionDepPdt, pdt_id: int):
    pdt = session.get(Product, pdt_id)
    if not pdt:
        raise HTTPException(status_code=404, detail="Product not found")
    try:
        session.delete(pdt)
        session.commit()
    except Exception as e:
        print(f"Catching: {e}")
        return {"ok": False}
    return {"ok": True}

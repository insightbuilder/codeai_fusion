# pyright: reportGeneralTypeIssues=false

from fastapi import FastAPI
from redis_om import Migrator, get_redis_connection, HashModel

app = FastAPI()

redis = get_redis_connection(
    host="34.229.80.21",
    port="6379",
)


class Product(HashModel):
    name: str
    price: float
    quantity: int

    # class Meta:
    #     database: redis


Migrator(redis).run()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/products")
def all():
    # return []
    return Product.all_pks()

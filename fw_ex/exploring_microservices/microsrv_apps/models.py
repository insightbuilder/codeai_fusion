from redis_om import get_redis_connection, Migrator, HashModel

redis = get_redis_connection(
    host="34.229.80.21",
    port=6379,
    decode_response=True,
)


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database: redis


if __name__ == "__main__":
    product = Product(name="Laptop", price=999.99, quantity=10)
    product.save()

    retrieved = Product.get(product.pk)
    print(retrieved)

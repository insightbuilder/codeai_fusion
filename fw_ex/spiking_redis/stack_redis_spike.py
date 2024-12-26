import redis
import numpy as np
import json
from redis.commands.search.field import TagField, TextField, VectorField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query

redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
redis_client.flushdb()

microwave = {
    "brand": "Samsung",
    "model": "SM-1000",
    "color": "white",
    "price": "$1000",
    "features": {
        "size": "large",
        "weight": "heavy",
    },
}

redis_client.execute_command("JSON.SET", "microwave:brand", ".", json.dumps(microwave))

mdata = redis_client.execute_command("JSON.GET", "microwave:brand")

print(mdata)

redis_client.execute_command(
    "JSON.SET", "microwave:json:1", ".", '{"brand": "Samsung", "color": "maroon"}'
)

print(redis_client.execute_command("JSON.GET", "microwave:brand", "price"))

redis_client.execute_command("JSON.SET", "microwave:brand", "price", "577")
redis_client.execute_command(
    "JSON.SET", "microwave:brand", ".features.weight", '"taxi"'
)

print(redis_client.execute_command("JSON.GET", "microwave:brand", "price"))

print(redis_client.execute_command("JSON.GET", "microwave:json:1"))

# Delete the color field
redis_client.execute_command("JSON.DEL", "microwave:json:1", "$.features.color")
# Seems some of the versions don't support delte
redis_client.execute_command("JSON.DEL", "microwave:json:1")
print(redis_client.execute_command("JSON.GET", "microwave:json:1"))


## Working on redis search

index_def = IndexDefinition(prefix=["microwave"], index_type=IndexType.HASH)

redis_client.ft("microwaveIDX").create_index(
    [
        TextField("brand"),
        TextField("model"),
        TagField("features"),
    ],
    definition=index_def,
)

redis_client.hset(
    "microwave:1",
    mapping={
        "brand": "Samsung",
        "model": "SM-1000",
        "features": "power:1000w,color:Black",
    },
)

redis_client.hset(
    "microwave:2",
    mapping={
        "brand": "Ornid",
        "model": "S-5000",
        "features": "power:500w,color:Whik",
    },
)

result = redis_client.ft("microwaveIDX").search("Ornid")

print(result)

result = redis_client.ft("microwaveIDX").search(
    "Samsung",
    # filter="@features:{color:Whik}",
)
print(result)

index_name = "index"
doc_prefix = "doc:"


def create_idx(vec_dim: int):
    try:
        redis_client.ft(index_name).info()
        print("Index already exists")
    except:
        schema = (
            TagField("tag"),
            VectorField(
                "vector",
                "FLAT",
                {
                    "DIM": vec_dim,
                    "TYPE": "FLOAT32",
                    "DISTANCE_METRIC": "COSINE",
                },
            ),
        )

        definition = IndexDefinition(prefix=[doc_prefix], index_type=IndexType.HASH)
        redis_client.ft(index_name).create_index(schema, definition=definition)
        print("Index created")


vec_dim = 1536

create_idx(vec_dim)

pipe = redis_client.pipeline()

obj = [
    {"name": "a", "tag": "a"},
    {"name": "b", "tag": "b"},
    {"name": "c", "tag": "c"},
]

for bj in obj:
    key = f"doc:{bj['name']}"
    bj["vector"] = np.random.rand(vec_dim).astype(np.float32).tobytes()
    pipe.hset(key, mapping=bj)

res = pipe.execute()


query = (
    Query("*=>[KNN 2 @vector $vec as score]")
    .sort_by("score")
    .return_fields("id", "score")
    # .return_field("vector", decode_field=False)  # return the vector field as bytes
    .paging(0, 2)
    .dialect(2)
)

query_params = {
    "vec": np.random.rand(vec_dim).astype(np.float32).tobytes(),
    "radius": 0.2,
}

print(redis_client.ft(index_name).search(query, query_params).docs)

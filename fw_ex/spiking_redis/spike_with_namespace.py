from redis import Redis
import json

# pyright: reportOptionalMemberAccess=false

redis_client = Redis(host="localhost", port=6379, db=0)
redis_client.flushdb()

redis_client.set("name:god", "loki")
redis_client.set("name:asari", "tany")
redis_client.set("robot:geth:walker", "Robin")
redis_client.set("robot:king", "kong")
redis_client.set("robot:queen", "bee")
redis_client.set("animal:pet", "cerebrus")
redis_client.set("animal:wild", "giraffe")

# redis_client.get("name:god")
print("Name: ", redis_client.get("name:god").decode())

redis_client.hset("users:1", "name", "ting")
redis_client.hset("users:1", "place", "tong")

print(redis_client.hget("users:1", "name").decode())

redis_client.hset("users:2", mapping={"name": "ming", "place": "moon"})

print(redis_client.hget("users:2", "name").decode())

for key in redis_client.scan_iter("robot:*"):
    print(redis_client.get(key).decode())

redis_client.lpush("cups:porcelain", "cup1", "cup2", "cup3")
redis_client.lpush("cups:plastic", "cup1", "cup2", "cup3")
redis_client.lpush("cups:glass", "cup1", "cup2", "cup3")

for list in redis_client.scan_iter("cups:*"):
    print(redis_client.lrange(list, 0, -1))

for key in redis_client.scan_iter("animal:*"):
    print(redis_client.get(key).decode())

for key in redis_client.scan_iter("users:*"):
    print(redis_client.hgetall(key))

redis_client.hset("microwave:brand", "brand", "whirlpool")
redis_client.hset("microwave:brand", "cost", "$1000")

print(json.dumps(str(redis_client.hgetall("microwave:brand"))))

# microwave = json.loads(str(redis_client.hgetall("microwave:brand")))

microwave = {
    key.decode("utf-8"): value.decode("utf-8")
    for key, value in redis_client.hgetall("microwave:brand").items()
}


print(microwave["brand"])
print(microwave)

redis_client.sadd("bags:local", "bag1_local", "bag2_local", "bag3_local")
redis_client.sadd("bags:foreign", "bag1_foreign", "bag2_foreign", "bag3_foriegn")

for set in redis_client.scan_iter("bags:*"):
    print(redis_client.smembers(set))

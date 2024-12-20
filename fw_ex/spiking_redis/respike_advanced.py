import redis
import time
import json

client = redis.Redis(host="localhost", port=6379, db=0)

print("Test ping:", client.ping())

client.flushdb()

client.set("name", "loki")

print("Name:", client.get("name").decode())
# k = dict(nsrs=5)

k = 5
client.mset({"asm": k, "rns": 9, "mlf": 6})

print(client.keys())

print("Multi get: ", client.mget("asm", "rns", "mlf"))

client.set("counter", 1)

client.incr("counter")

client.decr("counter")
client.decr("counter")
client.decr("counter")
client.decr("counter")

print("Counter: ", client.get("counter").decode())

client.delete("counter")
try:
    print("Counter: ", client.get("counter").decode())

except Exception as e:
    print("errr", e)

client.hset("user:1", mapping={"name": "yob", "age": 23})
client.hset("user:2", mapping={"name": "bsm", "age": 51})

print(client.hgetall("user:1").items())
print(client.hget("user:1", "name").decode())

client.lpush("tasks", "t1", "t2", "t3")
client.rpush("tasks", "t5")

print(client.lrange("tasks", 0, -1))
client.lpop("tasks")
client.rpop("tasks")

print(client.lrange("tasks", 0, -1))

client.sadd("fruits", "apple", "banana")

print(client.smembers("fruits"))

client.srem("fruits", "banana")
print(client.smembers("fruits"))

client.zadd("testosrt", {"t": 5, "s": 7, "o": 9})

client.zrange("testosrt", 0, -1, withscores=True)

client.zadd("testosrt", {"t": 5, "s": 7, "o": 9})

print(client.zrange("testosrt", 0, -1, withscores=True))

client.zrem("testosrt", "s")
print(client.zrange("testosrt", 0, -1, withscores=True))

print(client.zscore("testosrt", "t"))

client.set("genie", "bottle", ex=5)
time.sleep(3)
print(client.get("genie"))

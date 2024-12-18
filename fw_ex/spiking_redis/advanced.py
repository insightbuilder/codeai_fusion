import redis
import time

client = redis.Redis(host="localhost", port=6379, db=0)

print("Pinger: ", client.ping())

# clear database index

client.flushdb()

print("Check key exists: ", client.exists("name"))

# basic strings

client.set("name", "bottle")

print("Name: ", client.get("name").decode("utf-8"))

client.mset({"a": 1, "b": 5, "c": 7})

print("Multi get: ", client.mget("a", "b", "c"))

# value increment

client.set("counter", 1)

client.incr("counter")

print("Counter: ", client.get("counter").decode())

try:
    client.incr("name")
    print("Name: ", client.get("name").decode())
except redis.exceptions.RedisError as e:
    print(e)

getkeys = client.keys("*")
print("Keys: ", getkeys)

# initiating conn to different client.

client1 = redis.Redis(host="localhost", port=6379, db=1)

getkeys_1 = client1.keys("*")
print("Keys of idx 1: ", getkeys_1)

# removing key

client.delete("name")

getkeys = client.keys("*")
print("Keys after delete: ", getkeys)

## Working with the hashes

client.hset("user:1", mapping={"name": "Bob", "s_name": "Chloe", "age": 5})

print("User details: ", client.hget("user:1", "name").decode())

print("User details: ", client.hgetall("user:1"))

client.hdel("user:1", "name")

print("User details after hdel: ", client.hgetall("user:1"))

## Working with lists

client.lpush("tasks", "t1", "t2", "t3")

client.rpush("tasks", "t4")

client.lpush("tasks", "t5")

print("Tasks: ", client.lrange("tasks", 0, -1))

print("all keys", client.keys("*"))

# ---#
client.set("test", "me")

print("test: ", client.get("test").decode())

# ---#

print("Tasks: ", client.lrange("tasks", 0, -1))

# ---#

client.sadd("fruits", "apple", "banana")

print("Members of fruits: ", client.smembers("fruits"))

print("Check if member: ", client.sismember("fruits", "apple"))
print("Check if member: ", client.sismember("fruits", "kiwi"))

print("remove mems", client.srem("fruits", "apple"))
print("Check if apple is member after remove: ", client.sismember("fruits", "apple"))

client.zadd("leadme", {"a": 17, "b": 23, "c": 63})

print("leadme ascending: ", client.zrange("leadme", 0, -1, withscores=True))

listascend = client.zrange("leadme", 0, -1, withscores=True)

for key, val in listascend:
    print(key.decode(), val)

print("leadme descending: ", client.zrevrange("leadme", 0, -1, withscores=True))

print("Get a's score: ", client.zscore("leadme", "a"))

print("Increment a's score", client.zincrby("leadme", 2, "a"))

print("Get a's score after incr: ", client.zscore("leadme", "a"))

# --- #

# client.set("name", "bottle", ex=2)


# time.sleep(2)

# print("Name: ", client.get("name"))

# --- #

pipe = client.pipeline()

pipe.set("balme", 10)
pipe.incr("balme", 5)
pipe.decr("balme", 15)

pipe.execute()

print("Final Balance: ", client.get("balme"))

# --- #

for i in range(5):
    message = f"Message {i}"
    client.publish("channel1", message)
    time.sleep(1)
    print("sent", message)

# --- ! has to be a diff script ###
pubsub = client.pubsub()

pubsub.subscribe("channel1")

for message in pubsub.listen():
    print(message)

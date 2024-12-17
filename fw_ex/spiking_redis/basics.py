import redis

client = redis.StrictRedis(host="localhost", port=6379, db=0)

client.set("foo", "bar")
print(client.get("foo"))

client.set("username", "guestme")
print(client.get("username"))

# lets make some Lpush in lists

client.lpush("mylist", "first")
client.lpush("mylist", "second")
client.lpush("mylist", "third")
client.lpush("mylist", "fourth")

print(client.lrange("mylist", 0, -1))

print(client.keys())

client.lpush("tasks", "t1", "t2", "t3")
client.lpush("tasks", "t63")

print(client.lrange("tasks", 0, -1))

# Hash example

client.hset("user:100", "user", "guest")
client.hset("user:101", "admin", "password")

print(client.hget("user:101", "admin"))
print(client.hgetall("user:100"))

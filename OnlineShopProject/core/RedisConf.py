import redis

red = redis.StrictRedis('localhost', 6379, decode_responses=True)


import redis

redis_client = redis.StrictRedis('localhost', 6379, db=0, decode_responses=True)


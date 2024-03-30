import redis
from otp.models import TOTPDevice
from otp.totp import TOTP

red = redis.StrictRedis('localhost', 6379, decode_responses=True)


RedisConf.red.setex()
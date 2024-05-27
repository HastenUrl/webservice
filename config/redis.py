import os
import redis

def create_redis():
  return redis.ConnectionPool(
    host=os.getenv("REDIS_HOST"), 
    port=os.getenv("REDIS_PORT"), 
    db=os.getenv("REDIS_DB"), 
    decode_responses=True
  )

def get_redis():
  return redis.Redis(connection_pool=create_redis())
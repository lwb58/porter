
import redis

__all__ = ["redis_client"]

pool = redis.ConnectionPool(host='redis', port=6379, decode_responses=True)
redis_client = redis.Redis(connection_pool=pool)

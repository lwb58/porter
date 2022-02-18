
import redis

__all__ = ["bilibili_redis", "sina_redis", "intl_redis"]

bilibili_redis = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
sina_redis = redis.Redis(host='redis', port=6379, db=1, decode_responses=True)
intl_redis = redis.Redis(host='redis', port=6379, db=2, decode_responses=True)


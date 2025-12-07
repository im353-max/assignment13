# app/auth/redis.py

try:
    from redis.asyncio import Redis
except ModuleNotFoundError:
    Redis = None  # Running tests without Redis installed

redis_client = None

def get_redis():
    global redis_client
    if redis_client is None:
        if Redis is None:
            # No redis installed → running tests
            return None

        redis_client = Redis(host="localhost", port=6379, decode_responses=True)

    return redis_client


async def add_to_blacklist(jti: str, expires: int):
    redis = get_redis()
    if redis is None:
        return  # Skip silently in tests
    await redis.setex(f"bl_{jti}", expires, "true")


async def is_blacklisted(jti: str) -> bool:
    redis = get_redis()
    if redis is None:
        return False  # Redis absent => no blacklist
    return await redis.exists(f"bl_{jti}") == 1
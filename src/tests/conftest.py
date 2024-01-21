import typing as t

import pytest
from fakeredis.aioredis import FakeRedis
from redis.asyncio import Redis


# Mock Redis connection
@pytest.fixture
def redis_conn():
    conn = t.cast(Redis, FakeRedis())
    return conn


# Mock for awaitable Redis
@pytest.fixture
def async_redis_mock(redis_conn):
    async def mock_redis_conn():
        return redis_conn

    return mock_redis_conn()

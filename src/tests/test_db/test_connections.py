import typing as t

import pytest
from fakeredis.aioredis import FakeRedis
from redis.asyncio import Redis
from redis.exceptions import ConnectionError

from db.connections import RedisConnector


def test_redis_connector_init(mocker, redis_conn):
    mocker.patch('redis.asyncio.Redis.from_url', return_value=redis_conn)
    connector = RedisConnector()
    assert connector._connection_to_await is not None and connector._connection is None


def test_redis_connector_init_fail(mocker):
    mocker.patch('redis.asyncio.Redis.from_url', side_effect=ConnectionError)
    with pytest.raises(ConnectionError):
        RedisConnector()


@pytest.mark.asyncio
async def test_redis_connector_context_manager(mocker, redis_conn, async_redis_mock):
    mocker.patch('redis.asyncio.Redis.from_url', return_value=async_redis_mock)
    async with RedisConnector() as conn:
        assert conn == redis_conn


@pytest.mark.asyncio
async def test_redis_connector_context_manager_close(
    mocker, redis_conn, async_redis_mock
):
    mocker.patch('redis.asyncio.Redis.from_url', return_value=async_redis_mock)
    mocker.spy(redis_conn, 'aclose')
    async with RedisConnector() as _:
        ...
    redis_conn.aclose.assert_awaited_once()

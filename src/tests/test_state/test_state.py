import orjson as json
import pytest
from numpy import zeros

import models
from core.config import settings
from core.enums import StateStorage
from core.exceptions import PathfinderError
from state.state import RedisStorage, State, get_state


@pytest.mark.asyncio
async def test_redis_storage(redis_conn, mocker):
    storage = RedisStorage(redis_conn)
    state = {
        'robot_id': {
            'field': {
                'maze': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                'current': [0, 0],
                'action_count': 0,
            },
            'action_count_log': [],
        }
    }
    mocker.spy(redis_conn, 'set')
    await storage.save_state(state)
    redis_conn.set.assert_called_once_with(
        settings.redis_server_state_key, json.dumps(state)
    )
    saved_state = await storage.retrieve_state()
    assert saved_state == state


@pytest.mark.asyncio
async def test_state(redis_conn, mocker):
    state = State(RedisStorage(redis_conn))
    entry = models.Entry(
        maze=zeros((3, 3), dtype=int),
        current=(0, 0),
        action_count=0,
        action_count_log=[],
    )  # Fill in with appropriate values
    mocker.spy(redis_conn, 'set')
    await state.set_state(entry)
    redis_conn.set.assert_called_once()

    assert await state.get_state() == entry


def test_get_state(mocker, redis_conn):
    mocker.patch.object(settings, 'state_storage', StateStorage.REDIS.value)
    assert isinstance(get_state(redis_conn), State)

    mocker.patch.object(settings, 'state_storage', 'unknown')
    with pytest.raises(PathfinderError):
        get_state(redis_conn)

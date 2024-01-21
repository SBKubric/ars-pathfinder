import typing as t
from unittest.mock import AsyncMock, MagicMock

import pytest
from fakeredis.aioredis import FakeRedis
from numpy import zeros
from redis.asyncio import Redis

from core.enums import Direction
from server.lib.pathfinder_pb2 import Field, MoveRequest, Point
from services.field_state import build_maze, moving, set_field
from state.state import get_state


@pytest.fixture
def mock_state():
    conn = t.cast(Redis, FakeRedis())
    return get_state(conn)


# Test for build_maze function
def test_build_maze():
    array = zeros((2, 2), dtype=int)
    assert build_maze(2, 2, 'O00O').tolist() == [[0, 0], [0, 0]]
    array[0, 1] = 1
    assert build_maze(2, 2, '0100').tolist() == [[0, 1], [0, 0]]


# Test for set_field function
@pytest.mark.asyncio
async def test_set_field(mock_state):
    field = Field(N=2, M=2, grid='O10O', source=Point(i=0, j=0))
    await set_field(mock_state, field)
    entry = await mock_state.get_state()
    assert entry.maze.tolist() == [[0, 1], [0, 0]]
    assert entry.current == (0, 0)


# Test for moving function
@pytest.mark.asyncio
async def test_moving(mocker, mock_state):
    field = Field(N=2, M=2, grid='O00O', source=Point(i=0, j=0))
    await set_field(mock_state, field)
    move_request = MoveRequest(targets=[Point(i=1, j=1)])
    executor = MagicMock()
    mocker.patch(
        'services.field_state.run_in_executor',
        AsyncMock(return_value=Direction.RIGHT.value),
    )
    response = await moving(mock_state, executor, move_request)
    assert response.direction == Direction.RIGHT

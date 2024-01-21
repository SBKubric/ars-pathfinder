import asyncio
import datetime
import logging
import typing as t
from concurrent.futures import ProcessPoolExecutor

from numpy import zeros
from numpy.typing import NDArray

import models
from core import exceptions as exc
from core.config import settings
from core.enums import Direction, GridValues
from pathfinder.finder import determine_direction
from server.lib.pathfinder_pb2 import Empty, Field, MoveRequest, MoveResponse
from services import validators
from state.state import State


def build_maze(n: int, m: int, grid: str) -> NDArray:
    """
    Builds a maze represented as a 2D array from a string representation.

    Parameters:
    n (int): The number of rows in the maze.
    m (int): The number of columns in the maze.
    grid (str): A string representation of the maze where 'O' represents an obstacle and '.' represents a free space.

    Returns:
    NDArray: A 2D numpy array representing the maze where 1 represents an obstacle and 0 represents a free space.
    """
    maze = zeros((n, m), dtype=int)
    for i in range(n):
        for j in range(m):
            if grid[i * m + j] == GridValues.OBSTACLE:
                maze[i][j] = 1
    return maze


async def set_field(state: State, field: Field) -> Empty:
    """
    Sets the state of the maze and the starting position of the robot.

    Parameters:
    state (State): The current state of the system.
    field (Field): An object containing the dimensions of the maze and its grid representation.

    Returns:
    Empty: An empty response indicating that the operation was successful.
    """
    validators.validate_field(field)

    maze = build_maze(field.N, field.M, field.grid)

    entity: models.Entry | None = await state.get_state()

    if not entity:
        entity = models.Entry(
            maze=maze,
            current=(field.source.i, field.source.j),
            action_count=0,
            action_count_log=[],
        )

    await state.set_state(entity)

    return Empty()


async def run_in_executor(executor, func, *args):
    """
    Runs a function in an executor and returns the result.

    For testing simplicity
    """
    return await asyncio.get_event_loop().run_in_executor(executor, func, *args)


async def moving(
    state: State, executor: ProcessPoolExecutor, move_request: MoveRequest
) -> MoveResponse:
    """
    Moves the robot according to the given request and updates the state accordingly.

    Parameters:
    state (State): The current state of the system.
    executor (ProcessPoolExecutor): An executor for running tasks in parallel.
    move_request (MoveRequest): An object containing the target positions for the robot.

    Returns:
    MoveResponse: An object containing the direction in which the robot should move next.
    """
    entry: models.Entry | None = await state.get_state()
    if not entry:
        raise exc.PathfinderError('State not found for robot!')

    maze: NDArray = t.cast(NDArray, entry.maze)
    targets: list[tuple[int, int]] = [(p.i, p.j) for p in move_request.targets]

    validators.validate_targets(maze.shape[0], maze.shape[1], move_request.targets)

    direction: int = await run_in_executor(
        executor, determine_direction, maze, entry.current, targets, settings.algo
    )

    entry.action_count += 1

    match direction:
        case Direction.ERROR:
            logging.error('Invalid direction!')
        case Direction.FINISH:
            entry.action_count_log.append(
                models.ActionCount(
                    count=entry.action_count, when=datetime.datetime.now()
                )
            )
        case Direction.RIGHT:
            entry.current = (entry.current[0], entry.current[1] + 1)
        case Direction.DOWN:
            entry.current = (entry.current[0] + 1, entry.current[1])
        case Direction.LEFT:
            entry.current = (entry.current[0], entry.current[1] - 1)
        case Direction.UP:
            entry.current = (entry.current[0] - 1, entry.current[1])

    await state.set_state(entry)

    return MoveResponse(direction=direction)  # type: ignore

import logging

from numpy.typing import NDArray

from core.enums import Direction
from pathfinder.managers import get_algo


def determine_direction(
    maze: NDArray, current: tuple[int, int], goals: list[tuple[int, int]], algo: str
) -> int:
    """
    Determine the direction to move based on the current position, goals, and algorithm.

    Parameters:
    maze (NDArray): The maze represented as a 2D array.
    current (tuple[int, int]): The current position in the maze.
    goals (list[tuple[int, int]]): The list of goal positions in the maze.
    algo (str): The name of the algorithm to use for determining the path.

    Returns:
    int: The direction to move next.

    Raises:
    ValueError: If the goals are not reachable or the current position is already at a goal.
    """

    algorithm = get_algo(algo)

    if not goals:
        return Direction.FINISH

    path: list[tuple[int, int]] | None = algorithm.search(maze, current, goals)

    if not path:
        if path is None:
            logging.error("Goals are not reachable")
        else:
            logging.error("Already in place")

        return Direction.ERROR

    where_to: tuple[int, int] = path[0]

    if where_to[0] > current[0]:
        return Direction.DOWN
    if where_to[0] < current[0]:
        return Direction.UP
    if where_to[1] > current[1]:
        return Direction.RIGHT
    if where_to[1] < current[1]:
        return Direction.LEFT

    logging.error("Unknown direction")
    return Direction.ERROR

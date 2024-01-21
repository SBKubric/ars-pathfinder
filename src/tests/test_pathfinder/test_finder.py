from numpy import zeros

from core.enums import AlgoValues, Direction
from pathfinder.a_star import AStar
from pathfinder.finder import determine_direction


def test_determine_direction_no_goals():
    maze = zeros((5, 5), dtype=int)
    current = (2, 2)
    goals = []
    algo = AlgoValues.ASTAR_MANHATTAN.value

    result = determine_direction(maze, current, goals, algo)
    assert result == Direction.FINISH


def test_determine_direction_invalid_path():
    maze = zeros((5, 5), dtype=int)
    current = (3, 3)
    goals = [(3, 3)]
    algo = AlgoValues.ASTAR_MANHATTAN.value

    result = determine_direction(maze, current, goals, algo)  # type: ignore
    assert result == Direction.ERROR


def test_determine_direction_valid_path(mocker):
    maze = zeros((5, 5), dtype=int)
    current = (2, 2)
    goals = [(3, 3)]
    algo = AlgoValues.ASTAR_MANHATTAN.value

    mocker.patch.object(AStar, 'search', return_value=[(3, 2)])
    result = determine_direction(maze, current, goals, algo)  # type: ignore
    assert result == Direction.DOWN

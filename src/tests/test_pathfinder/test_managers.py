import pytest

from pathfinder.a_star import AStar
from pathfinder.managers import Algorithm, get_algo


def test_algorithm_enum():
    assert Algorithm.ASTAR.value == 'astar'


def test_get_algo_with_valid_input():
    algo = get_algo('astar[manhattan]')
    assert isinstance(algo, AStar)


def test_get_algo_with_invalid_input():
    with pytest.raises(ValueError):
        get_algo('unknown[mode]')

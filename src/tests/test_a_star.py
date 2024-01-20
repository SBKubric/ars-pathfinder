import numpy as np
import pytest
from numpy.typing import NDArray

from pathfinder.a_star import Mode, distance, search

TEST_CASES = [
    {
        "name": "empty grid",
        "input": {
            "maze": [[0] * 5 for _ in range(5)],
            "start": (0, 0),
            "goals": [(4, 4)],
            "mode": Mode.MANHATTAN,
        },
        "output": [(1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)],
    },
    {
        "name": "single obstacle",
        "input": {
            "maze": [
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ],
            "start": (0, 0),
            "goals": [(4, 4)],
            "mode": Mode.MANHATTAN,
        },
        "output": [(1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)],
    },
    {
        "name": "multiple obstacles",
        "input": {
            "maze": [
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ],
            "start": (0, 0),
            "goals": [(4, 4)],
            "mode": Mode.MANHATTAN,
        },
        "output": [(1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)],
    },
    {
        "name": "Start and Goal are the same",
        "input": {
            "maze": [
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ],
            "start": (0, 0),
            "goals": [(0, 0)],
            "mode": Mode.MANHATTAN,
        },
        "output": [],
    },
    {
        "name": "Start and Goal are unreachable",
        "input": {
            "maze": [
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
            ],
            "start": (0, 0),
            "goals": [(4, 4)],
            "mode": Mode.MANHATTAN,
        },
        "output": None,
    },
    {
        "name": "Start and Goal are on diagonal ends",
        "input": {
            "maze": [
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ],
            "start": (0, 0),
            "goals": [(4, 4)],
            "mode": Mode.MANHATTAN,
        },
        "output": [(1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)],
    },
    {
        "name": "Start and Goal in Same Row",
        "input": {
            "maze": [
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ],
            "start": (0, 0),
            "goals": [(0, 4)],
            "mode": Mode.MANHATTAN,
        },
        "output": [
            (1, 0),
            (2, 0),
            (3, 0),
            (3, 1),
            (3, 2),
            (3, 3),
            (2, 3),
            (1, 3),
            (0, 3),
            (0, 4),
        ],
    },
    {
        "name": "Start and Goal in Same Column",
        "input": {
            "maze": [
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ],
            "start": (0, 0),
            "goals": [(4, 0)],
            "mode": Mode.MANHATTAN,
        },
        "output": [(1, 0), (2, 0), (3, 0), (4, 0)],
    },
]

PARAMETRIZE_ARGS = (
    "case_name,maze,start,goal,output,mode",
    [
        (
            case["name"],
            np.array(case["input"]["maze"], int),
            case["input"]["start"],
            case["input"]["goals"],
            case["output"],
            case["input"]["mode"],
        )
        for case in TEST_CASES
    ],
)


@pytest.mark.parametrize(*PARAMETRIZE_ARGS)
def test_a_star(
    case_name: str,
    maze: NDArray,
    start: tuple[int, int],
    goal: tuple[int, int],
    output: list[tuple[int, int]],
    mode: Mode,
):
    result = search(maze, start, goal)
    print(result)
    assert result == output


def test_manhattan_mode():
    assert distance((0, 0), (3, 4)) == 7


def test_euclidean_mode():
    assert distance((0, 0), (3, 4), Mode.EUCLIDEAN) == pytest.approx(5)


def test_diagonal_mode():
    assert distance((0, 0), (3, 4), Mode.DIAGONAL) == 4


def test_invalid_mode():
    with pytest.raises(ValueError):
        distance((0, 0), (3, 4), 'INVALID')  # type: ignore


def test_negative_coordinates():
    assert distance((-3, -4), (3, 4)) == 14

import abc
import typing as t

from numpy.typing import NDArray


class AlgorithmProtocol(t.Protocol):
    def __init__(self, mode: str = 'default', process_pool=None) -> None:
        """
        Args:
            mode (str, optional): The type of heuristic to be used. Defaults to 'default'.
        """
        ...

    @abc.abstractmethod
    def search(
        self, maze: NDArray, start: t.Tuple[int, int], goals: t.List[t.Tuple[int, int]]
    ) -> t.List[t.Tuple[int, int]] | None:
        """
        Implement the A* search algorithm.

        Args:
            maze (numpy.NDArray): The maze represented as a 2D array.
            start (tuple[int, int]): The start point.
            goals (list[tuple[int, int]]): The goal points.

        Returns:
            list[tuple[int, int]] | None: A list of tuples representing the path from the start point to the goal point, or None if no path exists.
        """
        ...

import enum
import logging

from pathfinder.a_star import AStar
from pathfinder.abstract import AlgorithmProtocol


class Algorithm(enum.Enum):
    """
    Enum representing the available algorithms.
    Currently only supports A* algorithm.
    """

    ASTAR = 'astar'


def get_algo(algo: str) -> AlgorithmProtocol:
    """
    Function to get the algorithm instance based on the input string.

    Parameters:
    algo (str): The name of the algorithm followed by its mode enclosed in square brackets. For example, 'astar[mode]'.

    Returns:
    AlgorithmProtocol: An instance of the requested algorithm.

    Raises:
    ValueError: If the requested algorithm is unknown.
    """
    algo, mode = algo[:-1].split('[')

    if algo == Algorithm.ASTAR.value:
        return AStar(mode)
    else:
        logging.error(f'Unknown algorithm: {algo}')
        raise ValueError(f'Unknown algorithm: {algo}')

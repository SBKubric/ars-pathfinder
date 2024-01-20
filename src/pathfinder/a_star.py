import enum
import heapq

from numpy.typing import NDArray


class Mode(str, enum.Enum):
    """
    Enum class for specifying the type of heuristic to be used in the A* search algorithm.

    Attributes:
        MANHATTAN: Use the Manhattan distance as the heuristic.
        EUCLIDEAN: Use the Euclidean distance as the heuristic.
        DIAGONAL: Use the maximum absolute difference between the coordinates as the heuristic.
    """

    MANHATTAN = "manhattan"
    EUCLIDEAN = "euclidean"
    DIAGONAL = "diagonal"


def distance(a: tuple[int, int], b: tuple[int, int], mode: Mode = Mode.MANHATTAN):
    """
    Calculate the heuristic distance between a and b according to the specified mode.

    Args:
        a (tuple[int, int]): The first point.
        b (tuple[int, int]): The second point.
        mode (Mode, optional): The type of heuristic to be used. Defaults to Mode.MANHATTAN.

    Returns:
        float: The heuristic distance.

    Raises:
        ValueError: If the mode is invalid.
    """

    if mode == Mode.MANHATTAN:
        return abs(b[0] - a[0]) + abs(b[1] - a[1])
    elif mode == Mode.EUCLIDEAN:
        return ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5
    elif mode == Mode.DIAGONAL:
        return max(abs(b[0] - a[0]), abs(b[1] - a[1]))
    else:
        raise ValueError("Invalid mode")


def heuristic(
    point: tuple[int, int], goals: list[tuple[int, int]], mode: Mode = Mode.MANHATTAN
):
    """
    Calculate the heuristic distance between point and the nearest goal according to the specified mode.

    Args:
        point (tuple[int, int]): The from point.
        goals (list[tuple[int, int]]): The list of goals.
        mode (Mode, optional): The type of heuristic to be used. Defaults to Mode.MANHATTAN.

    Returns:
        float: The distance to the nearest goal.

    Raises:
        ValueError: If the mode is invalid.
    """

    return min(distance(point, goal, mode) for goal in goals)


def search(
    maze: NDArray,
    start: tuple[int, int],
    goals: list[tuple[int, int]],
    mode: Mode = Mode.MANHATTAN,
) -> list[tuple[int, int]] | None:
    """
    Implement the A* search algorithm.

    Args:
        maze (numpy.NDArray): The maze represented as a 2D array.
        start (tuple[int, int]): The start point.
        goals (list[tuple[int, int]]): The goal points.
        mode (Mode, optional): The type of heuristic to be used. Defaults to Mode.MANHATTAN ("manhattan").

    Returns:
        list[tuple[int, int]] | None: A list of tuples representing the path from the start point to the goal point, or None if no path exists.
    """

    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    close_set = set()
    open_set = []

    gscore = {start: 0}
    fscore = {start: heuristic(start, goals, mode)}
    heapq.heappush(open_set, (fscore[start], start))

    came_from = {}
    while len(open_set) > 0:
        current = heapq.heappop(open_set)[1]

        if current in goals:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            data.reverse()
            return data

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + distance(current, neighbor, mode)

            if 0 <= neighbor[0] < maze.shape[0]:
                if 0 <= neighbor[1] < maze.shape[1]:
                    if maze[neighbor[0]][neighbor[1]] == 1:
                        # discard the neighbor which is an obstacle
                        continue
                else:
                    # discard the neighbor which is out of range
                    continue
            else:
                # discard the neighbor which is out of range
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                # discard the neighbor which is already in close_set
                continue

            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [
                i for i in open_set
            ]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goals, mode)
                heapq.heappush(open_set, (fscore[neighbor], neighbor))

    return None

import enum
import heapq

from numpy.typing import NDArray


class Mode(str, enum.Enum):
    MANHATTAN = "manhattan"
    EUCLIDEAN = "euclidean"
    DIAGONAL = "diagonal"


def heuristic(a: tuple[int, int], b: tuple[int, int], mode: Mode = Mode.MANHATTAN):
    if mode == Mode.MANHATTAN:
        return abs(b[0] - a[0]) + abs(b[1] - a[1])
    elif mode == Mode.EUCLIDEAN:
        return ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5
    elif mode == Mode.DIAGONAL:
        return max(abs(b[0] - a[0]), abs(b[1] - a[1]))
    else:
        raise ValueError("Invalid mode")


def a_star_search(
    maze: NDArray,
    start: tuple[int, int],
    goal: tuple[int, int],
    mode: Mode = Mode.MANHATTAN,
) -> list[tuple[int, int]] | None:
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    close_set = set()
    open_set = []

    gscore = {start: 0}
    fscore = {start: heuristic(start, goal, mode)}
    heapq.heappush(open_set, (fscore[start], start))

    came_from = {}
    while len(open_set) > 0:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            data.reverse()
            return data

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + heuristic(current, neighbor, mode)

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
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal, mode)
                heapq.heappush(open_set, (fscore[neighbor], neighbor))
    return None

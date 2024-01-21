import enum


class StateStorage(str, enum.Enum):
    REDIS = "redis"


class AlgoValues(str, enum.Enum):
    ASTAR_MANHATTAN = "astar[manhattan]"
    ASTAR_EUCLIDEAN = "astar[euclidean]"
    ASTAR_DIAGONAL = "astar[diagonal]"


class Direction(int, enum.Enum):
    ERROR = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    UP = 4
    FINISH = 5


class GridValues(str, enum.Enum):
    FREE = '0'
    OBSTACLE = '1'

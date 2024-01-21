import typing as t

from core.exceptions import PathfinderError
from server.lib.pathfinder_pb2 import Field, Point


def validate_field(field: Field):
    """
    Validates the given field.

    Args:
        field (Field): The field to validate.

    Raises:
        PathfinderError: If the field is invalid.
    """
    if not field.N > 0:
        raise PathfinderError('N must be greater than 0')
    if not field.M > 0:
        raise PathfinderError('M must be greater than 0')
    if len(field.grid) != field.N * field.M:
        raise PathfinderError('Grid length must be N * M')
    if not field.source.i >= 0:
        raise PathfinderError('Source i must be greater than or equal to 0')
    if not field.source.j >= 0:
        raise PathfinderError('Source j must be greater than or equal to 0')
    if not field.source.i < field.N:
        raise PathfinderError('Source i must be less than N')
    if not field.source.j < field.M:
        raise PathfinderError('Source j must be less than M')


def validate_targets(n: int, m: int, targets: t.Iterable[Point]):
    """
    Validates the given targets.

    Args:
        n (int): The number of rows in the grid.
        m (int): The number of columns in the grid.
        targets (Iterable[Point]): The targets to validate.

    Raises:
        PathfinderError: If any target is invalid.
    """
    for target in targets:
        if not target.i >= 0:
            raise PathfinderError('Target i must be greater than or equal to 0')
        if not target.j >= 0:
            raise PathfinderError('Target j must be greater than or equal to 0')
        if not target.i < n:
            raise PathfinderError('Target i must be less than N')
        if not target.j < m:
            raise PathfinderError('Target j must be less than M')

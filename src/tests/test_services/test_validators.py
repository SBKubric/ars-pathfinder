import pytest

from core.exceptions import PathfinderError
from server.lib.pathfinder_pb2 import Field, Point
from services.validators import validate_field, validate_targets


def test_validate_field():
    # Test with valid input
    field = Field(N=3, M=3, grid="000010000", source=Point(i=0, j=0))
    assert validate_field(field) is None

    # Test with invalid input
    with pytest.raises(PathfinderError):
        field = Field(N=-1, M=5, grid="000010000", source=Point(i=0, j=0))
        validate_field(field)


def test_validate_targets():
    # Test with valid input
    targets = [Point(i=0, j=0), Point(i=4, j=4)]
    assert validate_targets(5, 5, targets) is None

    # Test with invalid input
    with pytest.raises(PathfinderError):
        targets = [Point(i=-1, j=0), Point(i=4, j=4)]
        validate_targets(5, 5, targets)

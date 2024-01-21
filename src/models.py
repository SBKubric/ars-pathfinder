import datetime

from pydantic import BaseModel
from pydantic_numpy.model import NumpyModel  # type: ignore
from pydantic_numpy.typing import Np2DArrayInt32  # type: ignore


class ActionCount(BaseModel):
    count: int
    when: datetime.datetime


class Entry(NumpyModel):
    maze: Np2DArrayInt32
    current: tuple[int, int]
    action_count: int
    action_count_log: list[ActionCount]

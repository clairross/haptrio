"""Spring force constants and vectors."""

from typing import Final
from py5 import Py5Vector as PVector

K_WALL: Final[float] = 250
F_WALL: Final[PVector] = PVector(0, 0)
PEN_WALL: Final[PVector] = PVector(0, 0)

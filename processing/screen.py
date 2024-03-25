"""Screen class to define screen parameters."""

from typing import Final
from py5 import Py5Vector as PVector

PIXELS_PER_METER: Final[float] = 4000.0
BASE_FRAME_RATE: Final[int] = 120
SCREEN_PIXEL_WIDTH: Final[int] = 2000
SCREEN_PIXEL_HEIGHT: Final[int] = 1000
SCREEN_CENTER: Final[PVector] = PVector(SCREEN_PIXEL_WIDTH / 2, SCREEN_PIXEL_HEIGHT / 2)

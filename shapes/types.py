from py5 import SQUARE, PROJECT, ROUND, MITER, BEVEL, PIE, CHORD, OPEN
from typing import Literal

CIRCLE_BUTTON: Literal[20] = 20
CIRCLE: Literal[18] = 18
STROKE_STYLE_MAP: dict[str, int] = {
    "Square": SQUARE,
    "Project": PROJECT,
    "Round": ROUND,
}
STROKE_JOIN_STYLE_MAP: dict[str, int] = {"Miter": MITER, "Bevel": BEVEL, "Round": ROUND}
MODE_MAP: dict[str, int] = {"Pie": PIE, "Chord": CHORD, "Open": OPEN}

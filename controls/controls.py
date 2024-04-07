from enum import StrEnum
from typing import NamedTuple


class Control(StrEnum):
    """Enum for the controls."""

    MOVE = "Move"
    SELECT = "Select"


class KeyboardKey(StrEnum):
    """Enum for the keys."""

    W = "w"
    A = "a"
    S = "s"
    D = "d"
    SPACE = " "
    ENTER = "Enter"
    ESCAPE = "Escape"
    LEFT_ARROW = "Left"
    RIGHT_ARROW = "Right"
    UP_ARROW = "Up"
    DOWN_ARROW = "Down"


class ControllerState(NamedTuple):
    """Class to represent the state of a control."""

    movement: tuple[float, float]
    selection: bool

"""Modules for time scale enum."""

from enum import Enum


class TimeScale(Enum):
    """Enum for different time scales."""

    NANOSECONDS = (0,)
    MILLISECONDS = (1,)
    SECONDS = (2,)
    MINUTES = (3,)
    HOURS = (4,)

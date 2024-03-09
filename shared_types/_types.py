"""Shared types for use in other modules."""

from typing import Dict, List, Union

JSON = Union[
    Dict[str, "JSON"],
    List["JSON"],
    str,
    int,
    float,
    bool,
    None,
]

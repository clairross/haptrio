from py5 import (
    Py5Vector as PVector,
    Py5Color as Color,
    Py5Shape as PShape,
    SQUARE,
    PROJECT,
    ROUND,
    MITER,
    BEVEL,
    PIE,
    CHORD,
    OPEN,
    color,
    no_stroke,
)
from abc import ABC, abstractmethod
import json
import uuid
from collections import defaultdict
from shared_types._types import JSON

CIRCLE_BUTTON = 20
CIRCLE = 18
STROKE_STYLE_MAP = {"Square": SQUARE, "Project": PROJECT, "Round": ROUND}
STROKE_JOIN_STYLE_MAP = {"Miter": MITER, "Bevel": BEVEL, "Round": ROUND}
MODE_MAP = {"Pie": PIE, "Chord": CHORD, "Open": OPEN}


class Shape(ABC):
    shape_type: int
    shape: PShape
    visible: bool
    enabled: bool
    stroke_color: Color
    stroke_weight: float
    stroke_cap_style: int
    stroke_join_style: int
    id: str

    def __init__(
        self,
        shape_type: int,
        visible: bool = True,
        enabled: bool = True,
        stroke_color: Color = Color(0),
        stroke_weight: float = 0,
        stroke_cap_style: int = SQUARE,
        stroke_join_style: int = MITER,
        id: str = "",
    ):
        self.shape_type = shape_type
        self.visible = visible
        self.enabled = enabled
        self.stroke_color = stroke_color
        self.stroke_weight = stroke_weight
        self.stroke_cap_style = stroke_cap_style
        self.stroke_join_style = stroke_join_style

        if id != "":
            self.id = id
        else:
            self.id = str(uuid.uuid4())

    @classmethod
    def from_json(cls, shape_type: int, json: JSON) -> "Shape":
        stroke_color: Colour = Color(0)
        stroke_weight: float
        stroke_cap_style: int
        stroke_join_style: int
        stroke_weight: float
        stroke_cap_style: int
        stroke_join_style: int
        visible: bool = True
        enabled: bool = True
        id: str

        if json and "id" in json.keys():
            id = json["id"]
        else:
            id = ""

        if json and "stroke" in json:
            stroke = json["stroke"]

            stroke_color = cls.get_color_from_json(stroke, "color")
            stroke_weight = stroke["weight"]
            stroke_cap_style = STROKE_STYLE_MAP[stroke["cap"]]
            stroke_join_style = STROKE_JOIN_STYLE_MAP[stroke["join"]]
        else:
            stroke_color = color(0)
            stroke_weight = 1
            stroke_cap_style = SQUARE
            stroke_join_style = MITER
            no_stroke()

        return cls(
            shape_type,
            visible,
            enabled,
            stroke_color,
            stroke_weight,
            stroke_cap_style,
            stroke_join_style,
            id,
        )

    @abstractmethod
    def get_intersection_line(self, other: Shape):
        pass

    @abstractmethod
    def get_intersection_triangle(self, other: Shape):
        pass

    @abstractmethod
    def get_intersection_quad(self, other: Shape):
        pass

    @abstractmethod
    def get_intersection_rect(self, other: Shape):
        pass

    @abstractmethod
    def get_intersection_square(self, other: Shape):
        pass

    @abstractmethod
    def get_intersection_ellipse(self, other: Shape):
        pass

    @abstractmethod
    def get_intersection_arc(self, other: Shape):
        pass

    @abstractmethod
    def get_intersection_circle(self, other: Shape):
        pass

    @abstractmethod
    def get_position(self):
        pass

    @abstractmethod
    def translate(self, direction: PVector):
        pass

    @abstractmethod
    def print(self):
        pass

    def get_color_from_json(self, obj: JSON, key: str) -> Color:
        try:
            color_string: str = obj[key]
            if color_string.startswith("#"):
                color_string = color_string[1:]
            if len(color_string) == 6:
                color_string = "FF" + color_string
            return Color(color_string)
        except Exception as e:
            print(f"Error parsing color from JSON: {e}")
            return Color(0)

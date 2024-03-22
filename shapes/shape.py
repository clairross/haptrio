from py5 import (
    Py5Vector as PVector,
    Py5Color as Color,
    Py5Shape as PShape,
    SQUARE,
    LINE,
    ARC,
    ELLIPSE,
    RECT,
    QUAD,
    TRIANGLE,
    MITER,
    color,
    no_stroke,
    Sketch as PSketch,
)
from abc import ABC, abstractmethod
from processing.sketch_manager import SketchManager
from shared_types._types import JSON
from shapes.types import (
    CIRCLE,
    CIRCLE_BUTTON,
    STROKE_JOIN_STYLE_MAP,
    STROKE_STYLE_MAP,
)
from random import randint
from uuid import uuid4


class Shape(ABC):
    shape_type: int
    shape: PShape
    visible: bool
    enabled: bool
    stroke_color: Color
    stroke_weight: float
    stroke_cap_style: int
    stroke_join_style: int
    uuid: str
    sketch: PSketch

    def __init__(
        self,
        shape_type: int,
        visible: bool = True,
        enabled: bool = True,
        stroke_color: Color = color(0),
        stroke_weight: float = 0,
        stroke_cap_style: int = SQUARE,
        stroke_join_style: int = MITER,
        uuid: str = "",
    ):
        if uuid != "":
            self.uuid = uuid
        else:
            self.uuid = str(uuid4())

        self.sketch = SketchManager.get_current_sketch()
        self.shape_type = shape_type
        self.visible = visible
        self.enabled = enabled
        self.stroke_color = stroke_color
        self.stroke_weight = stroke_weight
        self.stroke_cap_style = stroke_cap_style
        self.stroke_join_style = stroke_join_style

    @classmethod
    def from_json(cls, shape_type: int, json: JSON) -> "Shape":
        stroke_color: Colour = color(0)
        stroke_weight: float
        stroke_cap_style: int
        stroke_join_style: int
        stroke_weight: float
        stroke_cap_style: int
        stroke_join_style: int
        visible: bool = True
        enabled: bool = True
        uuid: str

        if json and "id" in json.keys():
            uuid = json["id"]
        else:
            uuid = ""

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
            uuid,
        )

    def draw(self):
        if not self.visible:
            return

        print(f"Drawing shape {self.uuid} at {self.get_position()}")
        self.sketch.shape(self.shape)
        self.sketch.fill(randint(1, 255), randint(1, 255), randint(1, 255))
        print(f"Drawing square at {self.sketch.mouse_x}, {self.sketch.mouse_y}")
        self.sketch.square(self.sketch.mouse_x, self.sketch.mouse_y, 80)

    def get_intersection(self, other: "Shape") -> PVector:
        other_type = other.shape_type

        if other_type == CIRCLE or other_type == CIRCLE_BUTTON:
            return self.__get_intersection_circle(other)
        elif other_type == LINE:
            return self.__get_intersection_line(other)
        elif other_type == TRIANGLE:
            return self.__get_intersection_triangle(other)
        elif other_type == QUAD:
            return self.__get_intersection_quad(other)
        elif other_type == RECT:
            return self.__get_intersection_rect(other)
        elif other_type == SQUARE:
            return self.__get_intersection_square(other)
        elif other_type == ELLIPSE:
            return self.__get_intersection_ellipse(other)
        elif other_type == ARC:
            return self.__get_intersection_arc(other)
        else:
            raise NotImplementedError

    def __get_intersection_line(self, other: "Shape") -> PVector:
        raise NotImplementedError

    def __get_intersection_triangle(self, other: "Shape") -> PVector:
        raise NotImplementedError

    def __get_intersection_quad(self, other: "Shape") -> PVector:
        raise NotImplementedError

    def __get_intersection_rect(self, other: "Shape") -> PVector:
        raise NotImplementedError

    def __get_intersection_square(self, other: "Shape") -> PVector:
        raise NotImplementedError

    def __get_intersection_ellipse(self, other: "Shape") -> PVector:
        raise NotImplementedError

    def __get_intersection_arc(self, other: "Shape") -> PVector:
        raise NotImplementedError

    def __get_intersection_circle(self, other: "Shape") -> PVector:
        raise NotImplementedError

    @abstractmethod
    def get_position(self) -> PVector:
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
            return color(color_string)
        except Exception as e:
            print(f"Error parsing color from JSON: {e}")
            return color(0)

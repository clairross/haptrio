from py5 import (
    Py5Vector as PVector,
    color,
    Py5Color as Color,
    ELLIPSE,
    get_current_sketch,
)
from typing import List, Tuple, Union, Callable
from shapes.shape import Shape
from shared_types.types import JSON

sketch = get_current_sketch()


class Circle(Shape):
    center: PVector
    radius: float
    diameter: float
    fill_color: Color
    initial_position: PVector

    def __init__(self, center: PVector, diameter: float, fill_color: Color):
        super().__init__(obj, CIRCLE)
        self.center = center
        self.diameter = diameter
        self.fill_color = fill_color
        self.radius = self.diameter / 2
        self.initial_position = self.center
        self.shape = sketch.create_shape(
            ELLIPSE, *self.center, self.diameter, self.diameter
        )

    @classmethod
    def from_json(cls, json: JSON) -> "Circle":
        fill_color = cls.get_color_from_json(cls, json, "fillColor")
        center = json["center"]
        diameter = obj["size"]

        return Circle(center, diameter, fill_color)

    def translate(self, direction: PVector):
        self.center = self.initial_position + direction

    def get_position(self) -> PVector:
        return self.center

    def get_fill_color(self) -> Color:
        return self.fill_color

    def get_center(self) -> PVector:
        return self.center

    def get_size(self) -> float:
        return self.diameter

    # ... other methods ...


class CircleButton(Circle):
    target_ids: List[str]

    def __init__(self, target_ids: List[str]):
        super().__init__(obj)
        self.target_ids = target_ids
        self.target = None
        self.on_intersect = None

    @classmethod
    def from_json(cls, json: JSON) -> "Circle":
        fill_color = cls.get_color_from_json(cls, json, "fillColor")
        center = json["center"]
        diameter = obj["size"]
        self.target_ids = obj["targetIds"]

        return Circle(center, diameter, fill_color)

    def get_intersection(self, other: "Shape") -> Union[Tuple[float, float], None]:
        intersection = super().get_intersection(other)

        if intersection is not None:
            self.disable()

        return intersection

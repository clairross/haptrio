from typing import List, Union
from py5 import (
    Py5Vector as PVector,
    RECT,
    CORNER,
    CORNERS,
    CENTER,
    RADIUS,
    SQUARE,
    MITER,
    Py5Color as Color,
    color,
)
from shapes.shape import Shape
from shapes.circle import Circle
from shared_types._types import JSON

RectMode = Union[CORNER, CORNERS, CENTER, RADIUS]


class Rectangle(Shape):
    center: PVector
    size: PVector
    top_left: PVector
    top_right: PVector
    bottom_right: PVector
    bottom_left: PVector
    vertices: List[PVector]
    original_vertices: List[PVector]
    rect_mode: RectMode
    fill_color: Color
    corner_radius: float

    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        corner_radius: float = 0,
        rect_mode: RectMode = CORNER,
        fill_color: Color = color(0),
        visible: bool = True,
        enabled: bool = True,
        stroke_color: Color = color(0),
        stroke_weight: float = 0,
        stroke_cap_style: int = SQUARE,
        stroke_join_style: int = MITER,
    ):
        super().__init__(
            RECT,
            visible=visible,
            enabled=enabled,
            fill_color=fill_color,
            stroke_color=stroke_color,
            stroke_weight=stroke_weight,
            stroke_cap_style=stroke_cap_style,
            stroke_join_style=stroke_join_style,
        )
        self.vertices = []
        self.original_vertices = []
        self.rect_mode = rect_mode
        self.fill_color = fill_color
        self.corner_radius = corner_radius

        if rect_mode == CORNER:
            self.center = PVector(x + width / 2, y + height / 2)
            self.size = PVector(width, height)
        elif rect_mode == CORNERS:
            self.center = PVector((x + width) / 2, (y + height) / 2)
            self.size = PVector(abs(x - width), abs(y - height))
        elif rect_mode == CENTER:
            self.center = PVector(x, y)
            self.size = PVector(width, height)
        elif rect_mode == RADIUS:
            self.center = PVector(x, y)
            self.size = PVector(width * 2, height * 2)

        self.top_left = PVector(
            self.center.x - self.size.x / 2, self.center.y - self.size.y / 2
        )
        self.top_right = PVector(
            self.center.x + self.size.x / 2, self.center.y - self.size.y / 2
        )
        self.bottom_right = PVector(
            self.center.x + self.size.x / 2, self.center.y + self.size.y / 2
        )
        self.bottom_left = PVector(
            self.center.x - self.size.x / 2, self.center.y + self.size.y / 2
        )
        self.vertices.append(self.top_left)
        self.vertices.append(self.top_right)
        self.vertices.append(self.bottom_right)
        self.vertices.append(self.bottom_left)
        self.original_vertices = self.vertices.copy()
        self.shape = self.sketch.create_shape(
            RECT,
            self.top_left.x,
            self.top_left.y,
            self.size.x,
            self.size.y,
            self.corner_radius,
        )
        self.update_shape_attributes()

    @classmethod
    def from_vectors(
        cls, position: PVector, size: PVector, rect_mode: RectMode = CORNER
    ) -> "Rectangle":
        return Rectangle(position.x, position.y, size.x, size.y, rect_mode=rect_mode)

    @classmethod
    def from_json(cls, json: JSON) -> "Rectangle":
        fill_color = cls.get_color_from_json(cls, json, "fillColor")
        center = json["center"]
        size = obj["size"]

        return Rectangle(center.x, center.y, size.x, size.y)

    def contains(self, point: PVector) -> bool:
        return (
            self.top_left.x <= point.x <= self.top_right.x
            and self.top_left.y <= point.y <= self.bottom_left.y
        )

    def translate(self, direction: PVector):
        self.vertices[0] = direction + self.original_vertices[0]
        self.vertices[1] = direction + self.original_vertices[1]
        self.vertices[2] = direction + self.original_vertices[2]
        self.vertices[3] = direction + self.original_vertices[3]
        self.center = self.center + direction

    def get_position(self):
        return self.center

    def get_vertices(self):
        return self.vertices

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def __get_intersection_circle(self, other: Circle):
        # center_x = self.center.x
        # center_y = self.center.y
        radius = other.radius
        current_center = self.vertices[0].copy() + self.size.copy() / 2

        x_intersects = abs(current_center.x - other.center.x) < (
            self.size.x / 2 + radius
        )
        y_intersects = abs(current_center.y - other.center.y) < (
            self.size.y / 2 + radius
        )

        if x_intersects and y_intersects:
            return PVector(0, 0)

        return None

    def __get_intersection_rect(self, other: "Shape") -> PVector:
        dx = abs(self.center.x - other.center.x)
        dy = abs(self.center.y - other.center.y)

        if dx > (other.size.x / 2 + self.size.x / 2) or dy > (
            other.size.y / 2 + self.size.y / 2
        ):
            return None

        if dx <= other.size.x / 2:
            x = other.center.x
        elif self.center.x < other.center.x:
            x = other.center.x - other.size.x / 2
        else:
            x = other.center.x + other.size.x / 2

        if dy <= other.size.y / 2:
            y = other.center.y
        elif self.center.y < other.center.y:
            y = other.center.y - other.size.y / 2
        else:
            y = other.center.y + other.size.y / 2

        return PVector(x, y)

    def print(self):
        print(
            f"Rectangle {self.uuid}: Center = {self.center} Size = {self.size} Vertices = {self.vertices}"
        )

from typing import List, Union
from py5 import (
    Py5Vector as PVector,
    QUAD,
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
from shared_types._types import JSON

RectMode = Union[CORNER, CORNERS, CENTER, RADIUS]


class Quadrilateral(Shape):
    center: PVector
    size: PVector
    vertices: List[PVector]
    original_vertices: List[PVector]
    rect_mode: RectMode
    fill_color: Color
    corner_radius: float

    def __init__(
        self,
        point_1_x: float,
        point_1_y: float,
        point_2_x: float,
        point_2_y: float,
        point_3_x: float,
        point_3_y: float,
        point_4_x: float,
        point_4_y: float,
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
            QUAD,
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

        x = min(point_1_x, point_2_x, point_3_x, point_4_x)
        y = min(point_1_y, point_2_y, point_3_y, point_4_y)
        width = max(point_1_x, point_2_x, point_3_x, point_4_x) - x
        height = max(point_1_y, point_2_y, point_3_y, point_4_y) - y

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

        self.vertices.append(PVector(point_1_x, point_1_y))
        self.vertices.append(PVector(point_2_x, point_2_y))
        self.vertices.append(PVector(point_3_x, point_3_y))
        self.vertices.append(PVector(point_4_x, point_4_y))
        self.original_vertices = self.vertices.copy()
        self.shape = self.sketch.create_shape()
        with self.shape.begin_closed_shape():
            for i, corner in enumerate(self.vertices):
                next_i = (i + 1) % len(self.vertices)
                prev_i = (i - 1) % len(self.vertices)
                next_corner = self.vertices[next_i]
                prev_corner = self.vertices[prev_i]
                control1 = PVector.lerp(corner, prev_corner, 1 - self.corner_radius)
                control2 = PVector.lerp(corner, next_corner, 1 - self.corner_radius)
                if i == 0:
                    self.shape.vertex(corner.x, corner.y)
                self.shape.bezier_vertex(
                    control1.x,
                    control1.y,
                    control2.x,
                    control2.y,
                    next_corner.x,
                    next_corner.y,
                )

        self.update_shape_attributes()

    @classmethod
    def from_vectors(
        cls, points: List[PVector], corner_radius: float = 0
    ) -> "Quadrilateral":
        assert len(points) == 4, "Quadrilateral must have 4 points"

        return Quadrilateral(
            points[0].x,
            points[0].y,
            points[1].x,
            points[1].y,
            points[2].x,
            points[2].y,
            points[3].x,
            points[3].y,
            corner_radius=corner_radius,
        )

    @classmethod
    def from_json(cls, json: JSON) -> "Quadrilateral":
        fill_color = cls.get_color_from_json(cls, json, "fillColor")
        points = json["points"]
        p1, p2, p3, p4 = points

        return Quadrilateral(
            p1[0],
            p1[1],
            p2[0],
            p2[1],
            p3[0],
            p3[1],
            p4[0],
            p4[1],
            fill_color=fill_color,
        )

    def contains(self, point: PVector) -> bool:
        x = point.x
        y = point.y
        inside = False
        j = len(self.vertices) - 1
        for i, vertex in enumerate(self.vertices):
            if (vertex.y > y) != (self.vertices[j].y > y) and x < (
                self.vertices[j].x - vertex.x
            ) * (y - vertex.y) / (self.vertices[j].y - vertex.y) + vertex.x:
                inside = not inside
            j = i
        return inside

    def translate(self, direction: PVector):
        self.vertices[0] = direction + self.original_vertices[0]
        self.vertices[1] = direction + self.original_vertices[1]
        self.vertices[2] = direction + self.original_vertices[2]
        self.vertices[3] = direction + self.original_vertices[3]
        self.center = self.center + direction

    def get_position(self) -> PVector:
        return self.center

    def get_vertices(self) -> List[PVector]:
        return self.vertices

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def print(self):
        print(f"Quadrilateral {self.uuid}: Vertices = {self.vertices}")

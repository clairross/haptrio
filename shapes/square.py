from typing import List, Dict, Any, Optional
from py5 import Py5Vector as PVector, Py5Color as Color, create_shape, fill, no_fill
from shapes.arc import Arc
from shapes.circle import Circle
from shapes.ellipse import Ellipse
from shapes.line import Line
from shapes.quadrilateral import Quadrilateral
from shapes.rectangle import Rectangle
from shapes.shape import Shape
from shapes.triangle import Triangle


class Square(Shape):
    vertices: List[PVector]
    center: PVector
    size: float
    fill_color: Color

    def __init__(self, obj: Dict[str, Any]):
        super().__init__(obj, SQUARE)
        self.vertices: List[PVector] = []
        self.center = PVector(obj["center"][0], obj["center"][1])
        self.size = obj["size"]
        if "fillColor" in obj:
            self.fill_color = self.get_color_from_json(obj, "fillColor")
            fill(self.fill_color)
        else:
            no_fill()
        first_vertex = PVector(
            self.center.x - self.size / 2, self.center.y - self.size / 2
        )
        second_vertex = PVector(
            self.center.x + self.size / 2, self.center.y - self.size / 2
        )
        third_vertex = PVector(
            self.center.x + self.size / 2, self.center.y + self.size / 2
        )
        fourth_vertex = PVector(
            self.center.x - self.size / 2, self.center.y + self.size / 2
        )
        self.center *= pixels_per_meter
        self.vertices.append(first_vertex * pixels_per_meter)
        self.vertices.append(second_vertex * pixels_per_meter)
        self.vertices.append(third_vertex * pixels_per_meter)
        self.vertices.append(fourth_vertex * pixels_per_meter)
        self.shape = create_shape(
            RECT,
            self.center.x,
            self.center.y,
            self.size * pixels_per_meter,
            self.size * pixels_per_meter,
        )

    def translate(self, direction: PVector) -> None:
        for vertex in self.vertices:
            vertex.add(direction)
        self.center.add(direction)

    def get_position(self) -> PVector:
        return self.center

    def get_vertices(self) -> List[PVector]:
        return self.vertices

    def get_fill_color(self) -> Color:
        return self.fill_color

    def get_center(self) -> PVector:
        return self.center

    def get_size(self) -> float:
        return self.size

    def print(self) -> None:
        print(f"Square {self.id}: Center = {self.center} Size = {self.size}")

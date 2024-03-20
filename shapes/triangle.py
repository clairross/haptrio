from typing import List, Dict, Any, Optional
from py5 import Py5Vector as PVector, Py5Color as Color, create_shape, fill
from shapes.arc import Arc
from shapes.circle import Circle
from shapes.ellipse import Ellipse
from shapes.line import Line
from shapes.quadrilateral import Quadrilateral
from shapes.rectangle import Rectangle
from shapes.shape import Shape
from shapes.square import Square

class Triangle(Shape):
    vertices: List[PVector]
    fill_color: Color
    vertices: List[PVector]

    def __init__(self, obj: Dict[str, Any]):
        super().__init__(obj, TRIANGLE)
        self.vertices: List[PVector] = []
        self.fill_color: color = self.get_color_from_json(obj, "fillColor")
        fill(self.fill_color)
        self.shape = create_shape()
        points = obj["points"]
        p1, p2, p3 = points[0], points[1], points[2]
        first_vertex = PVector(p1[0], p1[1])
        second_vertex = PVector(p2[0], p2[1])
        third_vertex = PVector(p3[0], p3[1])
        self.vertices.append(first_vertex * pixels_per_meter))
        self.vertices.append(second_vertex * pixels_per_meter))
        self.vertices.append(third_vertex * pixels_per_meter))
        self.shape = self.create_shape(TRIANGLE, first_vertex.x, first_vertex.y, second_vertex.x, second_vertex.y, third_vertex.x, third_vertex.y)

    def translate(self, direction: PVector) -> None:
        for vertex in self.vertices:
            vertex.add(direction)

    def get_position(self) -> PVector:
        return PVector.lerp(PVector.lerp(self.vertices[0], self.vertices[2], 0.5), self.vertices[1], 0.5)

    def get_vertices(self) -> List[PVector]:
        return self.vertices

    def get_fill_color(self) -> Color:
        return self.fill_color

    def print(self) -> None:
        print(f"Triangle {self.id}: Vertices = {self.vertices}")

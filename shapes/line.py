from typing import List, Optional
import json
from pvector import PVector


class Line:
    def __init__(self, obj: str):
        self.vertices: List[PVector] = []
        self.obj = json.loads(obj)
        points = self.obj["points"]
        start = points[0]
        end = points[1]
        start_vector = PVector(start[0], start[1])
        end_vector = PVector(end[0], end[1])
        self.original_start = start_vector.copy()
        self.original_end = end_vector.copy()
        self.vertices.append(start_vector)
        self.vertices.append(end_vector)
        print(f"Start line: {start_vector}, End line: {end_vector}")

    def translate(self, direction: PVector):
        start_vector = self.vertices[0]
        end_vector = self.vertices[1]
        start_vector.set(PVector.add(direction, self.original_start))
        end_vector.set(PVector.add(direction, self.original_end))

    def get_position(self) -> PVector:
        return PVector.lerp(self.vertices[0], self.vertices[1], 0.5)

    def get_vertices(self) -> List[PVector]:
        return self.vertices

    def get_intersection_line(self, other: "Line") -> Optional[PVector]:
        return None

    def get_intersection_triangle(self, other: "Triangle") -> Optional[PVector]:
        return None

    def get_intersection_quad(self, other: "Quadrilateral") -> Optional[PVector]:
        return None

    def get_intersection_rect(self, other: "Rectangle") -> Optional[PVector]:
        return None

    def get_intersection_square(self, other: "Square") -> Optional[PVector]:
        return None

    def get_intersection_ellipse(self, other: "Ellipse") -> Optional[PVector]:
        return None

    def get_intersection_arc(self, other: "Arc") -> Optional[PVector]:
        return None

    def get_intersection_circle(self, other: "Circle") -> Optional[PVector]:
        return None

    def print(self):
        print(f"Line {self.id}: Start = {self.vertices[0]} End = {self.vertices[1]}")

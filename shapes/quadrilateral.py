from typing import List, Optional
from dataclasses import dataclass


class Quadrilateral(Shape):
    def __init__(self, obj):
        super().__init__(obj, "QUAD")
        self.vertices = []
        self.fillColor = self.get_color_from_json(obj, "fillColor")
        points = obj["points"]
        p1, p2, p3, p4 = points
        first_vertex = PVector(p1[0], p1[1])
        second_vertex = PVector(p2[0], p2[1])
        third_vertex = PVector(p3[0], p3[1])
        fourth_vertex = PVector(p4[0], p4[1])
        self.vertices.append(first_vertex)
        self.vertices.append(second_vertex)
        self.vertices.append(third_vertex)
        self.vertices.append(fourth_vertex)

    def translate(self, direction: PVector):
        for vertex in self.vertices:
            vertex.add(direction)

    def get_position(self) -> PVector:
        return PVector.lerp(self.vertices[0], self.vertices[2], 0.5)

    def get_vertices(self) -> List[PVector]:
        return self.vertices

    def get_fill_color(self):
        return self.fillColor

    def get_intersection_line(self, line) -> Optional[PVector]:
        return line.get_intersection_quad(self)

    def get_intersection_triangle(self, triangle) -> Optional[PVector]:
        return triangle.get_intersection_quad(self)

    def get_intersection_quad(self, quad) -> Optional[PVector]:
        return quad.get_intersection_quad(self)

    def get_intersection_rect(self, rect) -> Optional[PVector]:
        return rect.get_intersection_quad(self)

    def get_intersection_ellipse(self, ellipse) -> Optional[PVector]:
        return ellipse.get_intersection_quad(self)

    def get_intersection_arc(self, arc) -> Optional[PVector]:
        return arc.get_intersection_quad(self)

    def get_intersection_square(self, other) -> Optional[PVector]:
        return None

    def get_intersection_circle(self, other) -> Optional[PVector]:
        return None

    def print(self):
        print(f"Quadrilateral {self.id}: Vertices = {self.vertices}")

    @staticmethod
    def get_color_from_json(obj, key):
        # Implement this method based on how you want to extract color from the JSON object
        pass

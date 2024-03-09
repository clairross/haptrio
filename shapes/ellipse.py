from typing import Optional
import json
from pvector import PVector


class Ellipse(Shape):
    def __init__(self, obj: str):
        super().__init__(obj, "ELLIPSE")
        self.fill_color = self.get_color_from_json(obj, "fillColor")
        center = obj["center"]
        size = obj["size"]
        self.center = PVector(center[0], center[1])
        self.size = PVector(size[0], size[1])
        self.center.mult(pixels_per_meter)
        self.size.mult(pixels_per_meter)

    def translate(self, direction: PVector):
        self.center.add(direction)

    def get_position(self) -> PVector:
        return self.center

    def get_fill_color(self) -> str:
        return self.fill_color

    def get_center(self) -> PVector:
        return self.center

    def get_size(self) -> PVector:
        return self.size

    def get_intersection_line(self, line: "Line") -> Optional[PVector]:
        return line.get_intersection_ellipse(self)

    def get_intersection_triangle(self, triangle: "Triangle") -> Optional[PVector]:
        return triangle.get_intersection_ellipse(self)

    def get_intersection_quad(self, quad: "Quadrilateral") -> Optional[PVector]:
        return quad.get_intersection_ellipse(self)

    def get_intersection_rect(self, rect: "Rectangle") -> Optional[PVector]:
        return rect.get_intersection_ellipse(self)

    def get_intersection_ellipse(self, ellipse: "Ellipse") -> Optional[PVector]:
        return ellipse.get_intersection_ellipse(self)

    def get_intersection_arc(self, arc: "Arc") -> Optional[PVector]:
        return arc.get_intersection_ellipse(self)

    def get_intersection_square(self, square: "Square") -> Optional[PVector]:
        return None

    def get_intersection_circle(self, circle: "Circle") -> Optional[PVector]:
        # The code for intersection between an ellipse and a circle is not provided
        # You need to implement this method based on your requirements
        return None

    def print(self):
        print(f"Ellipse {self.id}: Center = {self.center}, Size = {self.size}")

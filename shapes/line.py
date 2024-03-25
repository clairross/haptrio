from py5 import LINE, Py5Vector as PVector, Py5Color as Color, color
from typing import List
from shapes.shape import Shape
from shared_types._types import JSON


class Line(Shape):
    vertices: List[PVector]

    def __init__(
        self,
        start: PVector,
        end: PVector,
        thickness: float = 1,
        line_color: Color = color(0),
    ):
        super().__init__(LINE)
        self.vertices = [start, end]

        self.shape = self.sketch.create_shape(LINE, start.x, start.y, end.x, end.y)
        self.shape.begin_shape()
        self.shape.vertex(start.x, start.y)
        self.shape.vertex(end.x, end.y)
        self.shape.end_shape()
        self.shape.set_stroke(line_color)
        self.shape.set_stroke_weight(thickness)

    @classmethod
    def from_json(cls, json: JSON) -> "Line":
        start_json = json["start"]
        end_json = json["end"]
        thickness = json["thickness"] or 1
        line_color = cls.get_color_from_json(cls, json, "lineColor")
        diameter = obj["size"]

        return Line(
            PVector(end_json[0], end_json[1]),
            PVector(end_json[0], end_json[1]),
            thickness,
            line_color,
        )

    def translate(self, direction: PVector):
        start_vector = self.vertices[0]
        end_vector = self.vertices[1]
        start_vector.set(PVector.add(direction, self.original_start))
        end_vector.set(PVector.add(direction, self.original_end))

    def get_position(self) -> PVector:
        return PVector.lerp(self.vertices[0], self.vertices[1], 0.5)

    def print(self):
        print(f"Line {self.uuid}: Start = {self.vertices[0]} End = {self.vertices[1]}")

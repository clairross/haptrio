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

    def print(self):
        print(f"Ellipse {self.id}: Center = {self.center}, Size = {self.size}")

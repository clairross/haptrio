from typing import Optional
import json
from pvector import PVector


class Arc(Shape):
    def __init__(self, obj: str):
        super().__init__(obj, "ARC")
        self.fill_color = (
            self.get_color_from_json(obj, "fillColor") if "fillColor" in obj else None
        )
        center = obj["center"]
        size = obj["size"]
        self.start_angle = radians(obj["startAngle"])
        self.end_angle = radians(obj["endAngle"])
        self.mode = mode_map[obj["mode"]]
        self.center = PVector(center[0], center[1])
        self.size = PVector(size[0], size[1])
        self.center.mult(pixels_per_meter)
        self.size.mult(pixels_per_meter)

    def contains(self, point: PVector) -> bool:
        return False

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
        print(
            f"Arc {self.id}: Center = {self.center}, Size = {self.size}, Start Angle = {self.start_angle}, End Angle = {self.end_angle}, Mode = {self.mode}"
        )

from py5 import Py5Vector as PVector, color, Py5Color as Color, ELLIPSE
from typing import List, Tuple, Union, Callable
from shapes.shape import Shape
from shapes.types import CIRCLE
from shared_types._types import JSON


class Circle(Shape):
    center: PVector
    radius: float
    diameter: float
    fill_color: Color
    initial_position: PVector

    def __init__(self, center: PVector, diameter: float, fill_color: Color):
        super().__init__(CIRCLE)
        self.center = center
        self.diameter = diameter
        self.fill_color = fill_color
        self.radius = self.diameter / 2
        self.initial_position = self.center
        self.shape = self.sketch.create_shape(
            ELLIPSE, self.center.x, self.center.y, self.diameter, self.diameter
        )
        self.shape.set_fill(self.fill_color)

    @classmethod
    def from_json(cls, json: JSON) -> "Circle":
        fill_color = cls.get_color_from_json(cls, json, "fillColor")
        center = json["center"]
        diameter = obj["size"]

        return Circle(center, diameter, fill_color)

    def contains(self, point: PVector) -> bool:
        return point.dist(self.center) <= self.radius

    def translate(self, direction: PVector):
        self.center = self.initial_position + direction
        self.shape.translate(direction.x, direction.y)

    def get_position(self) -> PVector:
        return self.center

    def get_fill_color(self) -> Color:
        return self.fill_color

    def get_center(self) -> PVector:
        return self.center

    def get_size(self) -> float:
        return self.diameter

    def __get_intersection_line(self, line: "Line") -> Union[PVector, None]:
        # Calculate the distance between the circle center and the line
        distance = line.distance_to_point(self.center)

        # Check if the distance is less than or equal to the radius
        if distance <= self.radius:
            # Calculate the penetration distance
            penetration = self.radius - distance

            # Calculate the direction vector from the line to the circle center
            direction = line.closest_point_to_point(self.center) - self.center
            direction.normalize()

            # Return the direction vector multiplied by the penetration distance
            return direction * penetration
        else:
            return None

    def __get_intersection_rect(self, rect: "Rectangle") -> Union[PVector, None]:
        dx = abs(self.center.x - rect.center.x)
        dy = abs(self.center.y - rect.center.y)

        if dx > (rect.width / 2 + self.radius) or dy > (rect.height / 2 + self.radius):
            return None

        if dx <= rect.width / 2:
            x = rect.center.x
        elif self.center.x < rect.center.x:
            x = rect.center.x - rect.width / 2
        else:
            x = rect.center.x + rect.width / 2

        if dy <= rect.height / 2:
            y = rect.center.y
        elif self.center.y < rect.center.y:
            y = rect.center.y - rect.height / 2
        else:
            y = rect.center.y + rect.height / 2

        distance = self.center.dist(PVector(x, y))
        penetration = self.radius - distance

        if penetration >= 0:
            direction = PVector(x, y) - self.center
            direction.normalize()
            return direction * penetration
        else:
            return None

    def __get_intersection_square(self, square: "Square") -> Union[PVector, None]:
        distance = self.center.dist(square.center)
        penetration = self.radius + square.side_length / 2 - distance
        if penetration > 0:
            direction = square.center - self.center
            direction.normalize()
            return direction * penetration
        else:
            return None

    def __get_intersection_circle(self, circle: "Circle") -> Union[PVector, None]:
        distance = self.center.dist(circle.center)
        penetration = self.radius + circle.radius - distance
        if penetration > 0:
            direction = circle.center - self.center
            direction.normalize()
            return direction * penetration
        else:
            return None

    def print(self):
        print(f"Circle {self.uuid}: Center = {self.center}, Diameter = {self.diameter}")


class CircleButton(Circle):
    target_ids: List[str]

    def __init__(self, target_ids: List[str]):
        super().__init__(obj)
        self.target_ids = target_ids
        self.target = None
        self.on_intersect = None

    @classmethod
    def from_json(cls, json: JSON) -> "Circle":
        fill_color = cls.get_color_from_json(cls, json, "fillColor")
        center = json["center"]
        diameter = obj["size"]
        self.target_ids = obj["targetIds"]

        return Circle(center, diameter, fill_color)

    def get_intersection(self, other: "Shape") -> Union[Tuple[float, float], None]:
        intersection = super().get_intersection(other)

        if intersection is not None:
            self.disable()

        return intersection

from typing import Tuple
from collisions.collision_layer import CollisionLayer


class CollidableItem:
    layer: CollisionLayer

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        layer: CollisionLayer = CollisionLayer.DEFAULT,
    ):
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.layer = layer

    def get_bounding_box(self) -> Tuple[int, int, int, int]:
        return self.x, self.y, self.width, self.height

    def on_collision(self, other: "CollidableItem") -> None:
        raise NotImplementedError

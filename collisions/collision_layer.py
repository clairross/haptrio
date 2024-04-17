from enum import Enum


class CollisionLayer(Enum):
    DEFAULT = 0
    PLAYER = 1


CollisionLayerMatrix = {
    CollisionLayer.DEFAULT: [CollisionLayer.DEFAULT, CollisionLayer.PLAYER],
    CollisionLayer.PLAYER: [CollisionLayer.DEFAULT],
}

from typing import List, Tuple
from collisions.quadtree import QuadTree
from collisions.collidable_item import CollidableItem


class CollisionManager:
    def __init__(self, width: int, height: int):
        CollisionManager.width: int = width
        CollisionManager.height: int = height
        CollisionManager.quadtree: QuadTree = QuadTree(0, 0, width, height)

    @staticmethod
    def add_item(item: CollidableItem) -> None:
        if not CollisionManager.quadtree:
            return

        CollisionManager.quadtree.insert(item)

    @staticmethod
    def remove_item(item: CollidableItem) -> None:
        if not CollisionManager.quadtree:
            return

        CollisionManager.quadtree.remove(item)

    def update(self) -> List[Tuple[CollidableItem, CollidableItem]]:
        if not CollisionManager.quadtree:
            return []

        return CollisionManager.quadtree.get_collisions()

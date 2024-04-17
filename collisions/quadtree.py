from collisions.collidable_item import CollidableItem
from collisions.collision_layer import CollisionLayerMatrix
from typing import List, Tuple


class QuadTree:
    MAX_ITEMS_PER_NODE: int = 4

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.items: List[CollidableItem] = []
        self.children: List[QuadTree] = []

    def insert(self, item: CollidableItem) -> None:
        if self._is_leaf_node():
            self.items.append(item)
            if len(self.items) > self.MAX_ITEMS_PER_NODE:
                self._split()
        else:
            child_index = self._get_child_index(item)
            if child_index != -1:
                self.children[child_index].insert(item)

    def remove(self, item: CollidableItem) -> None:
        if self._is_leaf_node():
            self.items = [i for i in self.items if i != item]
        else:
            child_index = self._get_child_index(item)
            if child_index != -1:
                self.children[child_index].remove(item)

    def get_collisions(self) -> List[Tuple[CollidableItem, CollidableItem]]:
        collisions: List[Tuple[CollidableItem, CollidableItem]] = []
        if self._is_leaf_node():
            for i, item1 in enumerate(self.items):
                print(f"Checking item {i} of {len(self.items)}")
                collisions.extend(
                    [
                        (item1, item2)
                        for item2 in self.items[i + 1 :]
                        if item2.layer in CollisionLayerMatrix[item1.layer]
                    ]
                )
        else:
            for child in self.children:
                if child != -1:
                    collisions.extend(child.get_collisions())
        return collisions

    def _is_leaf_node(self) -> bool:
        return len(self.children) == 0

    def _split(self) -> None:
        half_width: int = self.width // 2
        half_height: int = self.height // 2
        self.children[0] = QuadTree(self.x, self.y, half_width, half_height)
        self.children[1] = QuadTree(
            self.x + half_width, self.y, half_width, half_height
        )
        self.children[2] = QuadTree(
            self.x, self.y + half_height, half_width, half_height
        )
        self.children[3] = QuadTree(
            self.x + half_width, self.y + half_height, half_width, half_height
        )
        for item in self.items:
            child_index = self._get_child_index(item)
            if child_index != -1:
                self.children[child_index].insert(item)
        self.items = []

    def _get_child_index(self, item: CollidableItem) -> int:
        x, y, width, height = item.get_bounding_box()
        if (
            x + width <= self.x + self.width // 2
            and y + height <= self.y + self.height // 2
        ):
            return 0
        if x >= self.x + self.width // 2 and y + height <= self.y + self.height // 2:
            return 1
        if x + width <= self.x + self.width // 2 and y >= self.y + self.height // 2:
            return 2
        if x >= self.x + self.width // 2 and y >= self.y + self.height // 2:
            return 3

        return -1

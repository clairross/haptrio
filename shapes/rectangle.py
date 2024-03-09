from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass


class Rectangle(Shape):
    def __init__(self, obj):
        super().__init__(obj, "RECT")
        self.vertices = []
        self.originalVertices = []
        self.center = PVector(obj["center"][0], obj["center"][1])
        self.size = PVector(obj["size"][0], obj["size"][1])
        self.topLeft = PVector(
            self.center.x - self.size.x / 2, self.center.y - self.size.y / 2
        )
        self.topRight = PVector(
            self.center.x + self.size.x / 2, self.center.y - self.size.y / 2
        )
        self.bottomRight = PVector(
            self.center.x + self.size.x / 2, self.center.y + self.size.y / 2
        )
        self.bottomLeft = PVector(
            self.center.x - self.size.x / 2, self.center.y + self.size.y / 2
        )
        self.vertices.append(self.topLeft)
        self.vertices.append(self.topRight)
        self.vertices.append(self.bottomRight)
        self.vertices.append(self.bottomLeft)
        self.originalVertices.append(self.topLeft.copy())
        self.originalVertices.append(self.topRight.copy())
        self.originalVertices.append(self.bottomRight.copy())
        self.originalVertices.append(self.bottomLeft.copy())

    def Translate(self, direction):
        self.vertices[0] = direction + self.originalVertices[0]
        self.vertices[1] = direction + self.originalVertices[1]
        self.vertices[2] = direction + self.originalVertices[2]
        self.vertices[3] = direction + self.originalVertices[3]
        self.center.add(direction)

    def GetPosition(self):
        return self.center

    def GetVertices(self):
        return self.vertices

    def GetCenter(self):
        return self.center

    def GetSize(self):
        return self.size

    def GetIntersectionCircle(self, other):
        centerX = self.center.x
        centerY = self.center.y
        radius = other.radius
        current_center = self.vertices[0].copy() + self.size.copy() / 2

        x_intersects = abs(current_center.x - other.center.x) < (
            self.size.x / 2 + radius
        )
        y_intersects = abs(current_center.y - other.center.y) < (
            self.size.y / 2 + radius
        )

        if x_intersects and y_intersects:
            return PVector(0, 0)

        return None

    def Print(self):
        print(
            f"Rectangle {self.id}: Center = {self.center} Size = {self.size} Vertices = {self.originalVertices}"
        )

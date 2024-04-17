"""Screen class to define screen parameters."""

from typing import Callable, cast
from py5 import (
    Py5Vector as PVector,
    Sketch,
    Py5Image as Image,
    Py5Vector as PVector,
)
from processing.sketch_manager import SketchManager
from world_map.world import WORLD_PIXEL_WIDTH, WORLD_PIXEL_HEIGHT


class Screen:
    sketch: Sketch
    width: int
    height: int
    frame_rate: int
    center: PVector
    __screen_changed_callbacks: list[Callable[[int, int], None]]

    def __init__(self) -> None:
        self.width = WORLD_PIXEL_WIDTH
        self.height = WORLD_PIXEL_HEIGHT
        self.frame_rate = 120
        self.center = PVector(self.width / 2, self.height / 2)
        self.sketch = SketchManager.get_current_sketch()
        self.__screen_changed_callbacks = []

    def update(self) -> None:
        if self.sketch.width != self.width or self.sketch.height != self.height:
            # self.width = self.sketch.width
            # self.height = self.sketch.height
            self.window_size_changed()

        return

    def subscribe_to_window_changed(self, callback: Callable[[int, int], None]) -> None:
        self.__screen_changed_callbacks.append(callback)

    def unsubscribe_to_window_changed(
        self, callback: Callable[[int, int], None]
    ) -> None:
        self.__screen_changed_callbacks.remove(callback)

    def window_size_changed(self) -> None:
        for callback in self.__screen_changed_callbacks:
            callback(self.width, self.height)

    def set_window_title(self, title: str) -> None:
        self.sketch.window_title(title)

    def set_window_resizable(self, resizable: bool) -> None:
        self.sketch.window_resizable(resizable)

    def set_window_icon(self, path: str) -> None:
        self.sketch.get_surface().set_icon(
            self.sketch.load_image(path, dst=cast(Image, None))
        )

    def set_window_size(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.sketch.size(width, height)

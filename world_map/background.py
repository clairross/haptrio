from py5 import Sketch, Py5Vector as PVector, Py5Color as Color
from processing.sketch_manager import SketchManager


class Background:
    sketch: Sketch
    position: PVector
    background_color: Color

    def __init__(self, color: Color):
        self.sketch = SketchManager.get_current_sketch()
        self.background_color = color

    def draw(self):
        # self.sketch.background(self.image)
        self.sketch.background(self.background_color)

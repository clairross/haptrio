from py5 import Py5Image as Image, Sketch, CENTER
from typing import cast
from processing.sketch_manager import SketchManager


class Background:
    image_path: str
    image: Image = cast(Image, None)
    sketch: Sketch

    def __init__(self, image_path: str):
        self.sketch = SketchManager.get_current_sketch()
        self.image_path = image_path
        self.image = self.sketch.load_image(self.image_path, dst=self.image)
        print(f"Background image loaded: {self.image_path}")

    def draw(self):
        # self.sketch.background(self.image)
        self.sketch.background(255)
        self.sketch.push_matrix()
        self.sketch.rect_mode(CENTER)
        self.sketch.image(self.image, 0, 0)
        self.sketch.pop_matrix()

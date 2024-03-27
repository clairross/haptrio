from py5 import Py5Image as Image, Sketch, CENTER, Py5Vector as PVector
from typing import cast
from processing.sketch_manager import SketchManager
from world_map.world import WORLD_HALF_WIDTH


class Background:
    image_path: str
    image: Image = cast(Image, None)
    sketch: Sketch
    position: PVector

    def __init__(self, image_path: str):
        self.sketch = SketchManager.get_current_sketch()
        self.image_path = image_path
        self.image = self.sketch.load_image(self.image_path, dst=self.image)
        self.position = PVector(WORLD_HALF_WIDTH - self.image.width / 2, 0)
        print(f"Background image loaded: {self.image_path}")

    def draw(self):
        # self.sketch.background(self.image)
        self.sketch.background(255)
        self.sketch.push_matrix()
        self.sketch.rect_mode(CENTER)
        self.sketch.image(self.image, self.position.x, self.position.y)
        self.sketch.pop_matrix()

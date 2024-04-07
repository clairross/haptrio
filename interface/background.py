from py5 import Py5Image as Image, Sketch, CENTER, Py5Vector as PVector
from typing import cast
from processing.sketch_manager import SketchManager
from world_map.world import WORLD_HALF_WIDTH
from resources.resource_manager import ResourceManager, Resources
from shapes.rectangle import Rectangle


class Background:
    image_path: str
    image: Image = cast(Image, None)
    sketch: Sketch
    position: PVector
    selection_box: Image = cast(Image, None)
    note_inventory_background: Image = cast(Image, None)
    notes: list[Image]
    selection_box_container: Rectangle
    show_note_inventory: bool

    def __init__(self, image_path: str):
        resources: Resources = ResourceManager.get()
        self.sketch = SketchManager.get_current_sketch()
        self.image_path = image_path
        self.image = self.sketch.load_image(self.image_path, dst=self.image)
        self.note_inventory_background = self.sketch.load_image(
            resources.images.note_inventory_background,
            dst=self.note_inventory_background,
        )
        self.selection_box = self.sketch.load_image(
            resources.images.selection_box, dst=self.selection_box
        )
        self.position = PVector(WORLD_HALF_WIDTH - self.image.width / 2, 10)

        self.notes = []
        self.notes.append(self.sketch.load_image(resources.images.eighth_note))
        self.notes.append(self.sketch.load_image(resources.images.quarter_note))
        self.notes.append(self.sketch.load_image(resources.images.half_note))
        self.selection_box_container = Rectangle(
            WORLD_HALF_WIDTH - self.selection_box.width / 2,
            0,
            self.selection_box.width,
            self.selection_box.height,
        )
        self.show_note_inventory = False

        print(f"Background image loaded: {self.image_path}")

    def draw(self):
        # self.sketch.background(self.image)
        self.sketch.background(255)
        self.sketch.push_matrix()
        self.sketch.rect_mode(CENTER)
        self.sketch.image(self.image, self.position.x, self.position.y)
        self.sketch.image(
            self.selection_box, WORLD_HALF_WIDTH - self.selection_box.width / 2, 0
        )

        if self.show_note_inventory:
            self.sketch.image(
                self.note_inventory_background,
                WORLD_HALF_WIDTH - self.note_inventory_background.width / 2,
                200,
            )
            for i in range(3):
                self.sketch.image(self.notes[i], 900 + i * 100, 220)

        self.sketch.pop_matrix()

    def click(self, mouse_position: PVector):
        print("Selection box clicked")
        self.show_note_inventory = self.selection_box_container.contains(mouse_position)
        return True
    
    def hover(self, mouse_position: PVector):
        print("Hovered!*********************************************************************")

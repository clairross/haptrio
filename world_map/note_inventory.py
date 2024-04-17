from py5 import Py5Image as Image, Sketch, Py5Vector as PVector, color
from typing import cast
from processing.sketch_manager import SketchManager
from resources.resource_manager import ResourceManager, Resources, ImageParser
from shapes.rectangle import Rectangle
from audio.music_notes import NoteDuration


class NoteItem:
    duration: NoteDuration
    image: Image
    container: Rectangle
    is_hovered: bool

    def __init__(self, duration: NoteDuration, image: Image, container: Rectangle):
        self.duration = duration
        self.image = image
        self.container = container
        self.is_hovered = False
        self.sketch = SketchManager.get_current_sketch()


    def draw(self):
        with self.sketch.push():
            if self.is_hovered:
                self.sketch.fill(255, 0, 0, 60)
                self.container.draw()
                
            self.sketch.image(
                self.image,
                self.container.top_left.x,
                self.container.top_left.y,
            )




class NoteInventory:
    sketch: Sketch
    position: PVector
    show_note_inventory: bool
    container: Rectangle
    items: list[NoteItem]
    correct_answer: NoteDuration | None
    selected_correct_answer: bool | None
    PADDING: int = 10

    def __init__(self, position: PVector):
        self.sketch = SketchManager.get_current_sketch()
        self.note_inventory_background = ImageParser.get().note_inventory_background

        self.position = position
        self.show_note_inventory = True
        self.items = []
        self.correct_answer = None
        self.selected_correct_answer = None

        duration_images = {
            NoteDuration.HALF: ImageParser.get().half_note,
            NoteDuration.QUARTER: ImageParser.get().quarter_note,
            NoteDuration.EIGHTH: ImageParser.get().eighth_note,
        }

        next_position = position
        max_height: float = 0

        for note_duration in NoteDuration:
            duration_image = duration_images[note_duration]
            max_height = max(max_height, duration_image.height)

            self.items.append(
                NoteItem(
                    note_duration,
                    duration_image,
                    Rectangle(
                        next_position.x,
                        next_position.y,
                        duration_image.width,
                        duration_image.height,
                    ),
                ),
            )

            next_position = PVector(
                next_position.x + duration_image.width + 25,
                next_position.y,
            )

        self.container = Rectangle(
            position.x - self.PADDING,
            position.y - self.PADDING,
            self.items[-1].container.top_right.x - position.x + self.PADDING * 2,
            max_height + self.PADDING * 2,
            fill_color=color(205, 10, 205, 70),
        )

    def draw(self):
        with self.sketch.push():
            if self.show_note_inventory:
                self.container.draw()
                # self.sketch.image(
                #     self.note_inventory_background,
                #     self.position.x,
                #     self.position.y,
                # )

                for item in self.items:
                    item.draw()

                self.sketch.text_size(15)
                self.sketch.fill(0)
                self.sketch.text
                displayed_text = (
                    "Select a length to feel how long it plays:"
                    if not self.correct_answer
                    else (
                        f"How long does the selected note last?"
                        if self.selected_correct_answer is None
                        else (
                            f"Correct! The note is {'an eigth note.' if self.correct_answer == NoteDuration.EIGHTH
                                                    else 'a quarter note.' if self.correct_answer == NoteDuration.QUARTER
                                                    else 'a half note.' if self.correct_answer == NoteDuration.HALF
                                                    else ''}"
                            if self.selected_correct_answer
                            else "Try again!"
                        )
                    )
                )
                text_width = self.sketch.text_width(displayed_text)

                self.sketch.text(
                    displayed_text,
                    self.items[0].container.top_left.x - 50,
                    self.items[0].container.top_left.y - 15,
                )

    def reset(self):
        self.correct_answer = None
        self.selected_correct_answer = None

    def click(self, mouse_position: PVector):
        if self.selected_correct_answer:
            # Ignore clicks if the correct answer has been selected
            return True
        
        for item in self.items:
            if item.container.contains(mouse_position):
                self.selected_correct_answer = self.correct_answer == item.duration

        return self.selected_correct_answer or False

    
    def hover(self, mouse_position: PVector):
        for item in self.items:
            if not item.is_hovered and item.container.contains(mouse_position):
                item.is_hovered = True
            if item.is_hovered and not item.container.contains(mouse_position):
                item.is_hovered = False

    def set_current_problem(self, note_duration: NoteDuration):
        self.correct_answer = note_duration
        self.selected_correct_answer = None

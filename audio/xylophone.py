from py5 import Py5Color as Color, Py5Vector as PVector
from numpy import arange, flip
from shapes.rectangle import Rectangle
from shapes.quadrilateral import Quadrilateral
from typing import Literal
from audio.music_notes import MusicNote
from processing.sketch_manager import SketchManager
from threading import Timer
from audio.xylophone_key import XylophoneKey
from physics.force_generator import ForceGenerator
from collisions.collidable_item import CollidableItem
from physics.force_manager import ForceManager


class Xylophone(ForceGenerator):
    MIN_KEY_HEIGHT: Literal[50] = 140
    CORNER_RADIUS: Literal[10] = 10
    BACKING_HEIGHT_PERCENT: Literal[0.8] = 0.8
    OCTAVE_SIZE: Literal[8] = 8
    LOW_KEY: MusicNote = MusicNote.A
    HOVER_DAMPEN_FACTOR: Literal[0.05] = 0.05
    container: Rectangle
    keys: list[XylophoneKey]
    back_quadrilateral: Quadrilateral
    playing_keys: list[int]
    correct_answer: MusicNote | None
    selected_correct_answer: bool | None

    def __init__(
        self,
        container: Rectangle,
        num_keys: int,
        key_colors: list[Color],
        key_padding: float = 5,
    ) -> None:
        assert num_keys > 0, "Number of keys must be greater than 0"
        assert key_padding > 0, "Key padding must be greater than 0"
        assert container.size.x > 0, "Container width must be greater than 0"
        assert (
            container.size.y >= self.MIN_KEY_HEIGHT
        ), f"Container height must be greater than {self.MIN_KEY_HEIGHT}"
        self.playing_keys = []
        self.sketch = SketchManager.get_current_sketch()
        self.num_keys = num_keys
        self.key_colors = key_colors
        self.container = container
        self.correct_answer = None
        self.selected_correct_answer = None
        key_width = (container.size.x - (key_padding * (num_keys + 1))) / num_keys
        key_height_step = (container.size.y - self.MIN_KEY_HEIGHT) / num_keys
        key_heights = flip(
            arange(self.MIN_KEY_HEIGHT, container.size.y, key_height_step)
        )
        key_shapes = [
            Rectangle(
                container.top_left.x + key_padding + (i * (key_width + key_padding)),
                container.center.y - (key_heights[i] / 2),
                key_width,
                key_heights[i],
                corner_radius=self.CORNER_RADIUS,
                fill_color=self.key_colors[i % len(self.key_colors)],
                stroke_weight=5,
            )
            for i in range(num_keys)
        ]

        music_notes = [music_note.value for music_note in MusicNote]
        self.keys = [
            XylophoneKey(
                MusicNote(music_notes[(self.LOW_KEY.value + i) % self.OCTAVE_SIZE]),
                key_shapes[i],
            )
            for i in range(num_keys)
        ]

        ForceManager.add_force_generator(self)

    def draw(self):
        with self.sketch.push():
            self.sketch.fill(0)
            self.sketch.text_size(20)
            displayed_text = (
                "Select a key to hear what sound it makes:"
                if not self.correct_answer
                else (
                    f"What pitch does the selected key make?"
                    if self.selected_correct_answer is None
                    else (
                        f"Correct! The note is {self.correct_answer}"
                        if self.selected_correct_answer
                        else "Try again!"
                    )
                )
            )
            text_width = self.sketch.text_width(displayed_text)

            self.sketch.text(
                displayed_text,
                self.container.center.x - text_width / 2,
                self.container.top_left.y - 10,
            )

        for key in self.keys:
            key.draw()

    def reset(self):
        self.correct_answer = None
        self.selected_correct_answer = None

    def click(self, position: PVector):
        if self.selected_correct_answer:
            # Ignore clicks if the correct answer has been selected
            return True

        for key in self.keys:
            if key.contains(position):
                key.play()

                if self.correct_answer:
                    self.selected_correct_answer = self.correct_answer == key.node

        return self.selected_correct_answer or False

    def hover(self, position: PVector):
        for key in self.keys:
            key.hover(position)

    def on_collision(self, other: CollidableItem):
        [other_x, other_y, other_width, other_height] = other.get_bounding_box()
        other_position = Rectangle(
            other_x, other_y, other_width, other_height
        ).get_position()

        for key in self.keys:
            if key.contains(other_position):
                # TODO: key hover
                print(f"Key {key.node} is hovered")
                key.is_hovered = True
                pass
            else:
                key.is_hovered = False

    def get_current_force(self) -> PVector:
        for key in self.keys:
            if key.is_hovered:

                return (
                    key.vibration.get_next_magnitude()
                    * PVector.random(dim=2).normalize()
                    * self.HOVER_DAMPEN_FACTOR
                )

        return PVector(0, 0)

    def set_current_problem(self, musical_note: MusicNote):
        self.correct_answer = musical_note
        self.selected_correct_answer = None

from py5 import (
    Py5Color as Color,
    Py5Image as Image,
    RGB,
    HSB,
    color,
    Py5Vector as PVector,
)
from numpy import arange, flip
from shapes.rectangle import Rectangle
from shapes.quadrilateral import Quadrilateral
from typing import Literal
from audio.music_notes import MusicNotesAudio, MusicNote
from pygame.mixer import Sound
from resources.resource_manager import ResourceManager
from processing.sketch_manager import SketchManager
from threading import Timer


class Xylophone:
    MIN_KEY_HEIGHT: Literal[50] = 140
    CORNER_RADIUS: Literal[10] = 10
    BACKING_HEIGHT_PERCENT: Literal[0.8] = 0.8
    LOW_KEY: MusicNote = MusicNote.A
    container: Rectangle
    keys: list[Rectangle]
    key_sounds: list[Sound]
    image: Image
    back_quadrilateral: Quadrilateral
    playing_keys: list[int]

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
        resources = ResourceManager.get()
        self.image = self.sketch.load_image(resources.images.xylophone)
        self.num_keys = num_keys
        self.key_colors = key_colors
        self.container = container
        key_width = (container.size.x - (key_padding * (num_keys + 1))) / num_keys
        key_height_step = (container.size.y - self.MIN_KEY_HEIGHT) / num_keys
        key_heights = flip(
            arange(self.MIN_KEY_HEIGHT, container.size.y, key_height_step)
        )
        self.keys = [
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

        back_vertices = [
            container.top_left,
            container.top_right,
            container.bottom_right,
            container.bottom_left,
        ]

        self.back_quadrilateral = Quadrilateral(
            back_vertices[0].x,
            back_vertices[0].y,
            back_vertices[1].x,
            back_vertices[1].y,
            back_vertices[2].x,
            back_vertices[2].y,
            back_vertices[3].x,
            back_vertices[3].y,
            corner_radius=self.CORNER_RADIUS,
        )
        music_notes = [music_note.value for music_note in MusicNote]
        music_note_audio = MusicNotesAudio()
        self.key_sounds = [
            music_note_audio.get_note(
                MusicNote(music_notes[(self.LOW_KEY.value + i) % 7])
            )
            for i in range(0, num_keys)
        ]

    def draw(self):
        # self.sketch.image(
        #     self.image, self.container.top_left.x, self.container.top_left.y
        # )

        # self.back_quadrilateral.draw()

        for key in self.keys:
            key.draw()

    def click(self, mouse_position: PVector):
        for i, key in enumerate(self.keys):
            if key.contains(mouse_position):
                self.play_key(i)

    def play_key(self, key_index: int):
        if key_index in self.playing_keys:
            return

        def reset_color():
            self.keys[key_index].shape.set_fill(original_color)
            self.playing_keys.remove(key_index)

        self.playing_keys.append(key_index)
        original_color = self.keys[key_index].fill_color
        brighter_color = self.get_brighter_color(original_color)
        self.keys[key_index].shape.set_fill(brighter_color)
        timer = Timer(1, reset_color)
        timer.daemon = True
        timer.start()

        self.key_sounds[key_index].play()

    def get_brighter_color(self, old_color: Color, increase: int = 10):
        self.sketch.color_mode(HSB, 100)
        h = self.sketch.hue(old_color)
        s = self.sketch.saturation(old_color)
        b = self.sketch.brightness(old_color)
        b = min(100, b + increase)  # ensure brightness doesn't exceed 100
        brighter_color = color(h, s, b)
        self.sketch.color_mode(RGB, 255)  # switch back to default color mode
        return brighter_color

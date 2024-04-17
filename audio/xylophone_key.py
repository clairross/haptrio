from py5 import Py5Vector as PVector, Py5Color as Color, HSB, color, RGB
from threading import Timer
from shapes.rectangle import Rectangle
from pygame.mixer import Sound
from physics.vibration import Vibration
from audio.music_notes import MusicNote, MusicNotesAudio, MusicNoteWaveMagnitude
from processing.sketch_manager import SketchManager


class XylophoneKey:
    default_fill_color: Color
    container: Rectangle
    node: MusicNote
    note_sound: Sound
    is_playing: bool
    is_hovered: bool
    vibration: Vibration

    def __init__(self, note: MusicNote, container: Rectangle) -> None:
        self.sketch = SketchManager.get_current_sketch()
        self.vibration = Vibration(MusicNoteWaveMagnitude.get_wave_magnitude(note))
        self.note_sound = MusicNotesAudio.get_note(note)
        self.container = container
        self.default_fill_color = container.fill_color
        self.node = note
        self.is_playing = False
        self.is_hovered = False

    def draw(self) -> None:
        self.container.draw()

    def play(self) -> None:
        if self.is_playing:
            self.note_sound.stop()

        def reset_color():
            self.container.shape.set_fill(self.default_fill_color)
            self.is_playing = False

        brighter_color = self.get_brighter_color(self.default_fill_color)
        self.container.shape.set_fill(brighter_color)
        timer = Timer(1, reset_color)
        timer.daemon = True
        timer.start()
        self.is_playing = True
        self.note_sound.play()

    def contains(self, position: PVector) -> bool:
        return self.container.contains(position)

    def hover(self, mouse_position: PVector):
        if not self.is_hovered and self.container.contains(mouse_position):
            self.container.shape.set_fill(
                self.get_brighter_color(self.default_fill_color)
            )
            self.is_hovered = True
        elif self.is_hovered and not self.container.contains(mouse_position):
            self.container.shape.set_fill(self.default_fill_color)
            self.is_hovered = False

    def get_brighter_color(self, old_color: Color, increase: int = 10) -> Color:
        self.sketch.color_mode(HSB, 100)
        h = self.sketch.hue(old_color)
        s = self.sketch.saturation(old_color)
        b = self.sketch.brightness(old_color)
        b = min(100, b + increase)  # ensure brightness doesn't exceed 100
        brighter_color = color(h, s, b)
        self.sketch.color_mode(RGB, 255)  # switch back to default color mode
        return brighter_color

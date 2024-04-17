from py5 import (
    Py5Image as Image,
    Py5Vector as PVector,
    color,
    Py5Color as Color,
)
from audio.music_notes import MusicNote, NoteDuration, MusicNotesAudio
from resources.resource_manager import ImageParser
from processing.sketch_manager import SketchManager
from shapes.rectangle import Rectangle
from typing import cast
from scheduler.scheduler import Scheduler
from scheduler.timer_scale import TimeScale
from physics.vibration import Vibration
from pygame.mixer import Sound
from audio.music_notes import MusicNoteWaveMagnitude
from physics.force_generator import ForceGenerator
from physics.force_manager import ForceManager


class Note(ForceGenerator):
    music_note: MusicNote | None
    note_duration: NoteDuration
    duration_modifier: float
    note_color: Color
    is_playing: bool
    is_solvable: bool
    is_hovered: bool
    is_selected: bool
    is_solved: bool
    image: Image
    container: Rectangle
    position: PVector
    sound: Sound
    vibration: Vibration
    __playing_container_color: Color = color(0, 40, 200, 50)
    __solvable_container_color: Color = color(255, 250, 0, 50)
    __hovered_container_color: Color = color(165, 160, 0, 50)
    __selected_container_color: Color = color(95, 90, 0, 70)
    HOVERED_DAMPING = 0.2

    def __init__(
        self,
        music_note: MusicNote | None,
        note_duration: NoteDuration,
        note_color: Color,
        position: PVector,
        is_playing: bool = False,
        is_solvable: bool = False,
    ):
        self.music_note = music_note
        self.note_duration = note_duration
        self.note_color = note_color
        self.is_playing = is_playing
        self.is_solvable = is_solvable
        self.position = position
        self.is_solved = False
        self.is_hovered = False
        self.is_selected = False
        self.sketch = SketchManager.get_current_sketch()

        if note_duration == NoteDuration.EIGHTH:
            self.image = ImageParser.get().eighth_note
            self.duration_modifier = 0.5
        elif note_duration == NoteDuration.QUARTER:
            self.image = ImageParser.get().quarter_note
            self.duration_modifier = 1
        elif note_duration == NoteDuration.HALF:
            self.image = ImageParser.get().half_note
            self.duration_modifier = 2

        if music_note:
            self.sound = MusicNotesAudio.get_note(music_note)
            self.vibration = Vibration(
                MusicNoteWaveMagnitude.get_wave_magnitude(music_note)
            )

        self.container = Rectangle(
            position.x, position.y, self.image.width, self.image.height
        )

        ForceManager.add_force_generator(self)

    def draw(self):
        if self.is_playing:
            with self.sketch.push():
                self.container.shape.set_fill(self.__playing_container_color)
                self.container.draw()

        if self.is_selected:
            with self.sketch.push():
                self.container.shape.set_fill(self.__selected_container_color)
                self.container.draw()
        elif self.is_hovered:
            with self.sketch.push():
                self.container.shape.set_fill(self.__hovered_container_color)
                self.container.draw()
        elif self.is_solvable or self.is_solved:
            with self.sketch.push():
                self.container.shape.set_fill(self.__solvable_container_color)
                self.container.draw()

        if not self.is_solvable or self.is_solved:
            with self.sketch.push():
                self.sketch.tint(self.note_color)
                self.sketch.image(self.image, self.position.x, self.position.y)

    def play(self, tempo: int):
        self.is_playing = True
        duration = int(self.duration_modifier * 60 * 1000 / tempo)

        if not self.music_note:
            print(f"Resting for {duration} ms")
            self.current_vibration = cast(Vibration, None)
            return

        print(f"Playing note {self} for {duration} ms")
        channel = self.sound.play(maxtime=duration)

        def note_stopped():
            if channel.get_busy():
                return

            print("Note stopped")
            self.is_playing = False
            note_stopping_scheduler.stop()

        note_stopping_scheduler = Scheduler(
            10, note_stopped, time_scale=TimeScale.MILLISECONDS
        )
        note_stopping_scheduler.run()

    def get_current_force(self) -> PVector:
        if not self.music_note or not self.is_playing:
            return PVector(0, 0)

        random_force_vector = (
            PVector.random(dim=2).normalize() * self.vibration.get_next_magnitude()
        )

        if self.is_hovered:
            return self.HOVERED_DAMPING * random_force_vector

        return random_force_vector

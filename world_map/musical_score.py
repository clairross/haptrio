from py5 import (
    Py5Image as Image,
    Py5Vector as PVector,
    color,
)
from audio.music_notes import MusicNote, NoteDuration
from resources.resource_manager import (
    RawSongNote,
    ResourceManager,
    Resources,
)
from typing import cast
from processing.sketch_manager import SketchManager
from scheduler.scheduler import Scheduler
from scheduler.timer_scale import TimeScale
from queue import Queue
from random import sample
from world_map.note import Note
from world_map.world import WORLD_HALF_WIDTH, WORLD_HALF_HEIGHT


class MusicBar:
    notes: list[Note]

    def __init__(self) -> None:
        self.notes = []

    def __len__(self):
        return len(self.notes)

    def __getitem__(self, index: int):
        return self.notes[index]

    def __setitem__(self, index: int, value: Note):
        self.notes[index] = value

    def append(self, note: Note):
        self.notes.append(note)

    def __iter__(self):
        return iter(self.notes)

    def __reversed__(self):
        return reversed(self.notes)

    def __contains__(self, item: Note):
        return item in self.notes

    def __str__(self):
        return str(self.notes)

    def __repr__(self):
        return repr(self.notes)


class MusicalScore:
    """The score to display"""

    staff_image: Image
    notes: list[Note]
    position: PVector
    note_queue: Queue[Note]
    music_scheduler: Scheduler[None]
    is_playing: bool
    tempo: int
    bars: list[MusicBar]
    completed_problem: bool

    def __init__(self, position: PVector, song: list[RawSongNote], tempo: int = 120):
        self.music_scheduler = cast(Scheduler[None], None)
        resources: Resources = ResourceManager.get()
        self.sketch = SketchManager.get_current_sketch()
        self.staff_image = self.sketch.load_image(
            resources.images.staff, dst=cast(Image, None)
        )
        self.selection_box = self.sketch.load_image(
            resources.images.selection_box, dst=cast(Image, None)
        )
        self.position = position
        self.is_playing = False
        completed_problem = False

        self.tempo = tempo
        self.note_queue = Queue[Note]()
        self.difficulty = 1
        print(f"Queue size: {self.note_queue.qsize()}")
        note_colors = {
            "A": color("#Fd2828"),
            "B": color("#F9893b"),
            "C": color("#EEFB5D"),
            "D": color("#61D729"),
            "E": color("#51D2E3"),
            "F": color("#2E2AED"),
            "G": color("#B01B5A"),
            "C_SHARP": color("#Fd2828"),
            "Rest": color("#FFFFFF"),
        }
        string_to_pitch = {
            "A": MusicNote.A,
            "B": MusicNote.B,
            "C": MusicNote.C,
            "D": MusicNote.D,
            "E": MusicNote.E,
            "F": MusicNote.F,
            "G": MusicNote.G,
            "C_SHARP": MusicNote.C_SHARP,
            "Rest": None,
        }

        string_to_duration = {
            "Eighth": NoteDuration.EIGHTH,
            "Quarter": NoteDuration.QUARTER,
            "Half": NoteDuration.HALF,
        }

        music_bars: list[MusicBar] = []
        current_bar: MusicBar = MusicBar()
        current_bar_beat_count = 0
        bar_width = 350
        bar_height = 200
        self.notes = []

        for note, duration in song:
            note = Note(
                string_to_pitch[note],
                string_to_duration[duration],
                note_colors[note],
                PVector(
                    110
                    + self.position.x
                    + bar_width * current_bar_beat_count / 4
                    + (len(music_bars) % 3) * bar_width,
                    10 + self.position.y + bar_height * int(len(music_bars) / 3),
                ),
            )

            added_beat_count = (
                0.5
                if duration == "Eighth"
                else 1 if duration == "Quarter" else 2 if duration == "Half" else 0
            )

            current_bar.append(note)
            self.notes.append(note)

            if current_bar_beat_count + added_beat_count >= 4:
                music_bars.append(current_bar)
                current_bar = MusicBar()
                current_bar_beat_count = 0  # current_bar_beat_count - 4
            else:
                current_bar_beat_count += added_beat_count

        self.bars = music_bars

        # self.notes = [
        #     Note(
        #         string_to_pitch[note],
        #         string_to_duration[duration],
        #         note_colors[note],
        #         PVector(self.position.x + 50 + i * 50, self.position.y),
        #     )
        #     for i, (note, duration) in enumerate(song)
        # ]

    def generate_problem(self, difficulty: int):
        # Choose n random notes based on "level" (to be implemented)
        # Then replace the notes in the score with empty boxes but keep the note data
        random_notes = sample(self.notes, k=difficulty)

        for note in random_notes:
            note.is_solvable = True

        # set the rest of the notes to normal
        other_notes = [note for note in self.notes if note not in random_notes]
        for note in other_notes:
            note.is_solvable = False
            note.is_selected = False
            note.is_solved = False

    def update(self):
        self.completed_problem = all(
            [note.is_solved or not note.is_solvable for note in self.notes]
        )

    def draw(self):
        # self.sketch.background(self.image)
        with self.sketch.push():
            for i in range(int(len(self.bars) / 3 + 1)):
                self.sketch.image(
                    self.staff_image, self.position.x, self.position.y + i * 200
                )

            for note in self.notes:
                note.draw()

        with self.sketch.push():
            if self.completed_problem:
                self.sketch.text_size(52)
                self.sketch.fill(color(0, 255, 0))
                winning_text = "You won!"
                text_width = self.sketch.text_width(winning_text)
                self.sketch.text(
                    winning_text,
                    WORLD_HALF_WIDTH - text_width / 2,
                    WORLD_HALF_HEIGHT,
                )

    def play(self):
        if self.music_scheduler:
            self.music_scheduler.stop()
        note_durations = [
            int(note.duration_modifier * 60 * 1000 / self.tempo) for note in self.notes
        ]

        for note in self.notes:
            self.note_queue.put(note)

        def play_note():
            if self.note_queue.empty():
                self.is_playing = False

                if self.music_scheduler:
                    self.music_scheduler.stop()

                return

            note = self.note_queue.get()
            note.play(self.tempo)

        self.music_scheduler = Scheduler(
            note_durations, play_note, time_scale=TimeScale.MILLISECONDS
        )
        self.music_scheduler.run()
        self.is_playing = True

    def stop(self):
        if self.music_scheduler:
            self.music_scheduler.stop()
            self.is_playing = False
            self.note_queue = Queue[Note]()
            print(f"Queue size: {self.note_queue.qsize()}")

    def hover(self, position: PVector):
        for note in self.notes:
            if not note.is_solvable:
                continue

            if not note.is_hovered and note.container.contains(position):
                note.is_hovered = True
            if note.is_hovered and not note.container.contains(position):
                note.is_hovered = False

    def click(self, position: PVector) -> tuple[MusicNote, NoteDuration] | None:
        for note in self.notes:
            if (
                note.is_solvable
                and note.is_hovered
                and not note.is_solved
                and not note.is_selected
            ):
                note.is_selected = True

                for other_note in self.notes:
                    # Can't unselect unless you select another note
                    if other_note != note:
                        other_note.is_selected = False

                return (note.music_note, note.note_duration)

    def solved_current_selection(self):
        for note in self.notes:
            if note.is_selected:
                note.is_solved = True
                note.is_selected = False
                note.is_hovered = False
                note.is_solvable = False
                break

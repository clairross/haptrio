from resources.resource_manager import (
    ResourceManager,
    SoundResources,
    Resources,
)  # Adjust the import path as necessary
from pygame.mixer import Sound
from typing import Final
from enum import Enum


class MusicNote(Enum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6


class Octave(Enum):
    LOW = "Low"
    HIGH = "High"


class MusicNotesAudio:
    notes: Final[dict[MusicNote, Sound]]

    def __init__(self) -> None:

        resources: Resources = ResourceManager.get_resources()
        sound_paths: SoundResources = resources.sounds

        self.notes = {
            MusicNote.A: Sound(sound_paths.note_a),
            MusicNote.B: Sound(sound_paths.note_b),
            MusicNote.C: Sound(sound_paths.note_c),
            MusicNote.D: Sound(sound_paths.note_d),
            MusicNote.E: Sound(sound_paths.note_e),
            MusicNote.F: Sound(sound_paths.note_f),
            MusicNote.G: Sound(sound_paths.note_g),
        }

    def get_note(self, music_note: MusicNote) -> Sound:
        return self.notes.get(music_note)

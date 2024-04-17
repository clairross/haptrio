from py5 import color, Py5Vector as PVector
from resources.resource_manager import SongNoteParser
from world_map.background import Background
from audio.xylophone import Xylophone
from shapes.rectangle import Rectangle
from world_map.world import WORLD_HALF_WIDTH, WORLD_PIXEL_HEIGHT, WORLD_PIXEL_WIDTH
from world_map.musical_score import MusicalScore
from controls.controls import ControllerState
from controls.controllable import Controllable
from world_map.score_selection_area import ScoreSelectionArea
from world_map.note_inventory import NoteInventory
from world_map.difficulty_selector import DifficultySelector


class Scene(Controllable):
    """The map of the world.  This class is responsible for drawing the map"""

    background: Background
    xylophone: Xylophone
    musical_score: MusicalScore
    select_score_area: ScoreSelectionArea
    note_inventory: NoteInventory
    difficulty_selector: DifficultySelector

    def __init__(self):
        song = SongNoteParser.get().rain_rain_go_away
        self.background = Background(color="#F0F0F0")
        self.xylophone = Xylophone(
            Rectangle(WORLD_HALF_WIDTH - (580 / 2), WORLD_PIXEL_HEIGHT - 247, 580, 247),
            num_keys=8,
            key_colors=[
                color("#Fd2828"),
                color("#F9893b"),
                color("#EEFB5D"),
                color("#61D729"),
                color("#51D2E3"),
                color("#2E2AED"),
                color("#B01B5A"),
            ],
            key_padding=8,
        )

        controls_position = PVector(0, 450)
        self.select_score_area = ScoreSelectionArea(controls_position)

        self.difficulty_selector = DifficultySelector(
            controls_position + (100, self.select_score_area.size.y + 10),
            max_difficulty=len(song),
        )

        # WORLD_HALF_WIDTH - self.image.width / 2, 10)
        self.note_inventory = NoteInventory(
            PVector(WORLD_PIXEL_WIDTH - 200, WORLD_PIXEL_HEIGHT - 147)
        )
        self.musical_score = MusicalScore(
            PVector(80, 30),
            song,
            tempo=90,
        )
        self.musical_score.generate_problem(self.difficulty_selector.difficulty)

        return

    def control(self, control_state: ControllerState) -> None:
        if control_state.play and not self.musical_score.is_playing:
            print("Playing musical score")
            self.musical_score.play()

    # def input(self, key: KeyboardKey):
    #     if key == KeyboardKey.ENTER:
    #         self.musical_score.play()

    def click(self, mouse_position: PVector):
        correct_length_selected = self.note_inventory.click(mouse_position)
        correct_pitch_selected = self.xylophone.click(mouse_position)

        if correct_length_selected and correct_pitch_selected:
            self.musical_score.solved_current_selection()

        song = self.select_score_area.click(mouse_position)

        if song:
            self.xylophone.reset()
            self.note_inventory.reset()
            self.musical_score.stop()
            self.musical_score = MusicalScore(PVector(80, 30), song, tempo=90)
            self.difficulty_selector.update_max_score(len(song))
            self.musical_score.generate_problem(self.difficulty_selector.difficulty)

        changed_difficulty = self.difficulty_selector.click(mouse_position)

        print(f"Did change difficulty: {changed_difficulty}")

        if changed_difficulty:
            self.xylophone.reset()
            self.note_inventory.reset()
            self.musical_score.generate_problem(self.difficulty_selector.difficulty)

        correct_answer = self.musical_score.click(mouse_position)

        if correct_answer:
            self.xylophone.reset()
            self.note_inventory.reset()
            (correct_note, correct_duration) = correct_answer
            self.xylophone.set_current_problem(correct_note)
            self.note_inventory.set_current_problem(correct_duration)

    def hover(self, mouse_position: PVector):
        self.xylophone.hover(mouse_position)
        self.select_score_area.hover(mouse_position)
        self.difficulty_selector.hover(mouse_position)
        self.musical_score.hover(mouse_position)

    def draw(self):
        self.background.draw()
        self.xylophone.draw()
        self.musical_score.draw()
        self.select_score_area.draw()
        self.note_inventory.draw()
        self.difficulty_selector.draw()

    def update(self):
        self.musical_score.update()

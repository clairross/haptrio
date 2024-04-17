from py5 import Py5Vector as PVector
from typing import List
from shapes.rectangle import Rectangle
from resources.resource_manager import RawSongNote, SongNoteParser
from processing.sketch_manager import SketchManager


class Score:
    title: str
    song: List[RawSongNote]

    def __init__(self, title: str, song: List[RawSongNote]):
        self.title = title
        self.song = song


class ScoreButton:
    score: Score
    container: Rectangle
    is_hovered: bool

    def __init__(self, score: Score, container: Rectangle, is_hovered: bool):
        self.score = score
        self.container = container
        self.is_hovered = is_hovered


class ScoreSelectionArea:
    position: PVector
    score_selection_items: List[ScoreButton]
    size: PVector

    def __init__(self, position: PVector):
        self.sketch = SketchManager.get_current_sketch()
        self.position = position
        songs = SongNoteParser.get()
        button_size = PVector(300, 50)
        padding = 10

        self.score_selection_items = [
            ScoreButton(
                Score(
                    "When the Saints Go Marching In",
                    songs.when_the_saints_go_marching_in,
                ),
                Rectangle(
                    position.x, position.y, button_size.x, button_size.y, fill_color=255
                ),
                is_hovered=False,
            ),
            ScoreButton(
                Score("Rain Rain Go Away", songs.rain_rain_go_away),
                Rectangle(
                    position.x,
                    button_size.y + padding + position.y,
                    button_size.x,
                    button_size.y,
                    fill_color=255,
                ),
                is_hovered=False,
            ),
        ]

        self.size = PVector(
            button_size.x, len(self.score_selection_items) * (button_size.y + padding)
        )

    def draw(self):
        with self.sketch.push():
            self.sketch.text_size(15)
            self.sketch.fill(0)
            for score_selection_item in self.score_selection_items:
                score_selection_item.container.draw()
                self.sketch.fill(0)
                self.sketch.text(
                    score_selection_item.score.title,
                    score_selection_item.container.center.x - 50,
                    score_selection_item.container.center.y,
                )

        with self.sketch.push():
            self.sketch.fill(0)
            self.sketch.text_size(20)
            instructions_text = "Press enter to play the whole song"
            text_width = self.sketch.text_width(instructions_text)
            self.sketch.text(
                instructions_text,
                self.position.x,
                self.position.y - 20,
            )

    def click(self, mouse_position: PVector):
        self.sketch.circle(mouse_position.x, mouse_position.y, 20)

        for score_selection_item in self.score_selection_items:
            if score_selection_item.container.contains(mouse_position):
                print(f"Clicked on {score_selection_item.score.title}")
                return score_selection_item.score.song
        return None

    def hover(self, mouse_position: PVector):
        for score_selection_item in self.score_selection_items:
            if (
                not score_selection_item.is_hovered
                and score_selection_item.container.contains(mouse_position)
            ):
                score_selection_item.container.shape.set_fill(200)
                score_selection_item.is_hovered = True

            if (
                score_selection_item.is_hovered
                and not score_selection_item.container.contains(mouse_position)
            ):
                score_selection_item.container.shape.set_fill(255)
                score_selection_item.is_hovered = False

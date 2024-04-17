from py5 import Py5Vector as PVector, color
from shapes.circle import Circle
from processing.sketch_manager import SketchManager


class DifficultySelector:
    difficulty: int
    position: PVector
    up_difficulty_button: Circle
    down_difficulty_button: Circle
    is_hovering_up: bool
    is_hovering_down: bool
    text_width: float
    max_difficulty: int
    font_size: int = 20

    def __init__(self, position: PVector, max_difficulty: int):
        self.position = position
        self.sketch = SketchManager.get_current_sketch()
        self.difficulty = 1

        self.down_difficulty_button = Circle(position, 30, color(255))
        self.up_difficulty_button = Circle(position, 30, color(255))
        self.down_difficulty_button.shape.set_stroke_weight(2)
        self.up_difficulty_button.shape.set_stroke_weight(2)
        self.is_hovering_down = False
        self.is_hovering_up = False
        self.text_width = 0
        self.max_difficulty = max_difficulty
        self.font_size = 32

    def draw(self):
        difficulty_text = f"Difficulty: {self.difficulty}"

        with self.sketch.push():
            self.sketch.fill(0)
            self.sketch.text_size(15)
            self.text_width = self.sketch.text_width(difficulty_text)
            self.sketch.text(
                f"Difficulty: {self.difficulty}",
                self.position.x - self.text_width / 2,
                self.position.y,
            )

        with self.sketch.push():
            self.sketch.fill(0)
            plus_text_width = self.sketch.text_width("+")
            self.sketch.text_size(self.font_size)
            self.sketch.translate(self.text_width, 0)
            self.up_difficulty_button.draw()
            up_button_position = self.up_difficulty_button.get_position() + (0, 5)
            self.sketch.text(
                "+",
                up_button_position.x - plus_text_width / 2 - 3,
                up_button_position.y + 4,
            )

        with self.sketch.push():
            self.sketch.fill(0)
            minus_text_width = self.sketch.text_width("-")
            self.sketch.text_size(self.font_size)
            self.sketch.translate(-self.text_width, 0)
            self.down_difficulty_button.draw()
            down_button_position = self.down_difficulty_button.get_position() + (0, 5)
            self.sketch.text(
                "-",
                down_button_position.x - minus_text_width / 2 - 2,
                down_button_position.y + 3,
            )

    def update_max_score(self, max_score: int):
        self.max_difficulty = max_score

        if self.difficulty > self.max_difficulty:
            self.difficulty = self.max_difficulty

    def click(self, mouse_position: PVector) -> bool:
        did_change = False
        down_mouse_position = mouse_position + (self.text_width, 0)
        up_mouse_position = mouse_position - (self.text_width, 0)

        if self.down_difficulty_button.contains(down_mouse_position):
            self.difficulty -= 1
            did_change = True

        if self.up_difficulty_button.contains(up_mouse_position):
            self.difficulty += 1
            did_change = True

        if self.difficulty < 1:
            self.difficulty = 1
        if self.difficulty > self.max_difficulty:
            self.difficulty = self.max_difficulty

        return did_change

    def hover(self, mouse_position: PVector):
        down_mouse_position = mouse_position + (self.text_width, 0)
        up_mouse_position = mouse_position - (self.text_width, 0)

        if not self.is_hovering_down and self.down_difficulty_button.contains(
            down_mouse_position
        ):
            self.is_hovering_down = True
            self.down_difficulty_button.shape.set_fill(color(200))
        elif self.is_hovering_down and not self.down_difficulty_button.contains(
            down_mouse_position
        ):
            self.is_hovering_down = False
            self.down_difficulty_button.shape.set_fill(color(255))

        if not self.is_hovering_up and self.up_difficulty_button.contains(
            up_mouse_position
        ):
            self.is_hovering_up = True
            self.up_difficulty_button.shape.set_fill(color(200))
        elif self.is_hovering_up and not self.up_difficulty_button.contains(
            up_mouse_position
        ):
            self.is_hovering_up = False
            self.up_difficulty_button.shape.set_fill(color(255))

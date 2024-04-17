from py5 import Py5MouseEvent as MouseEvent, LEFT, CENTER, RIGHT
from controls.controller import Controller
from controls.controls import ControllerState


class Mouse(Controller):
    position: tuple[int, int]
    previous_position: tuple[int, int]
    left_key_pressed: bool
    right_key_pressed: bool
    middle_key_pressed: bool

    def __init__(self):
        super().__init__()
        self.previous_position = (0, 0)
        self.position = (0, 0)
        self.left_key_pressed = False
        self.right_key_pressed = False
        self.middle_key_pressed = False

    def update(self):
        super().update()
        self.previous_position = self.position

    def button_pressed(self, mouse_event: MouseEvent):
        print(f"Mouse pressed: {mouse_event}")
        mouse_button = mouse_event.get_button()

        if mouse_button == LEFT:
            self.left_key_pressed = True
        elif mouse_button == RIGHT:
            self.right_key_pressed = True
        elif mouse_button == CENTER:
            self.middle_key_pressed = True

    def button_released(self, mouse_event: MouseEvent):
        print(f"Mouse released: {mouse_event}")
        mouse_button = mouse_event.get_button()

        if mouse_button == LEFT:
            self.left_key_pressed = False
        elif mouse_button == RIGHT:
            self.right_key_pressed = False
        elif mouse_button == CENTER:
            self.middle_key_pressed = False

    def moved(self, mouse_event: MouseEvent):
        self.position = (mouse_event.get_x(), mouse_event.get_y())

    def get_state(self) -> ControllerState:
        movement: tuple[float, float] = (
            self.position[0] - self.previous_position[0],
            self.position[1] - self.previous_position[1],
        )

        return ControllerState(movement, self.left_key_pressed, False)

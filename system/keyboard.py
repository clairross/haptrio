from py5 import Py5KeyEvent as KeyEvent, CODED, ENTER, LEFT, RIGHT, UP, DOWN
from controls.controller import Controller
from controls.controls import ControllerState, KeyboardKey
from typing import cast


class Keyboard(Controller):
    __current_pressed_keys: set[KeyboardKey]

    def __init__(self):
        super().__init__()
        self.__current_pressed_keys = set()

    def key_pressed(self, key_event: KeyEvent):
        print(f"Key pressed: {key_event}")
        keyboard_key: KeyboardKey = self.__get_keyboard_key(key_event)

        if not keyboard_key:
            return

        self.__current_pressed_keys.add(keyboard_key)

    def key_released(self, key_event: KeyEvent):
        # print(f"Key released: {key_event}")
        keyboard_key: KeyboardKey = self.__get_keyboard_key(key_event)

        if not keyboard_key:
            return

        self.__current_pressed_keys.remove(keyboard_key)

    def get_state(self) -> ControllerState:
        movement: tuple[float, float] = (0, 0)

        if (
            KeyboardKey.UP_ARROW in self.__current_pressed_keys
            or KeyboardKey.W in self.__current_pressed_keys
        ):
            # Add the movement vector to tuple
            movement = (movement[0], movement[1] - 1)

        if (
            KeyboardKey.DOWN_ARROW in self.__current_pressed_keys
            or KeyboardKey.S in self.__current_pressed_keys
        ):
            movement = (movement[0], movement[1] + 1)

        if (
            KeyboardKey.LEFT_ARROW in self.__current_pressed_keys
            or KeyboardKey.A in self.__current_pressed_keys
        ):
            movement = (movement[0] - 1, movement[1])

        if (
            KeyboardKey.RIGHT_ARROW in self.__current_pressed_keys
            or KeyboardKey.D in self.__current_pressed_keys
        ):
            movement = (movement[0] + 1, movement[1])

        # Normalize the 2d movement vector
        magnitude = (movement[0] ** 2 + movement[1] ** 2) ** 0.5
        if magnitude != 0:
            movement = (movement[0] / magnitude, movement[1] / magnitude)

        selection = KeyboardKey.SPACE in self.__current_pressed_keys

        play_music = KeyboardKey.ENTER in self.__current_pressed_keys

        return ControllerState(movement, selection, play_music)

    def __get_keyboard_key(self, key_event: KeyEvent) -> KeyboardKey:
        key: str | int = cast(str, key_event.get_key())  # type: ignore

        if key == CODED:
            key = key_event.get_key_code()

            if key == LEFT:
                return KeyboardKey.LEFT_ARROW
            if key == RIGHT:
                return KeyboardKey.RIGHT_ARROW
            if key == UP:
                return KeyboardKey.UP_ARROW
            if key == DOWN:
                return KeyboardKey.DOWN_ARROW

        if key == ENTER:
            return KeyboardKey.ENTER
        if key == " ":
            return KeyboardKey.SPACE
        if key == "w":
            return KeyboardKey.W
        if key == "a":
            return KeyboardKey.A
        if key == "s":
            return KeyboardKey.S
        if key == "d":
            return KeyboardKey.D

        return cast(KeyboardKey, None)

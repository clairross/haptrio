from py5 import Py5Vector as PVector
from controls.controller import Controller
from haply.haply import Haply
from player.player import Player
from typing import cast


class HaplyController(Controller):
    player: Player
    haply: Haply
    input_direction: PVector
    __square_deadzone: float
    __initial_position: PVector

    def __init__(self, player: Player, haply: Haply, deadzone: float = 0.1):
        self.player = player
        self.haply = haply
        self.haply.subscribe(self.update_position)
        self.__square_deadzone = deadzone * deadzone
        self.__initial_position = cast(PVector, None)
        self.input_direction = PVector(0, 0)

    def update(self):
        # if self.input_direction.mag_sq < self.__square_deadzone:
        #     return

        print(f"Moving player by {self.input_direction}")
        self.player.move(self.input_direction)

    def update_position(self, position: PVector) -> None:
        if not self.__initial_position:
            self.__initial_position = position

        self.input_direction = position - self.__initial_position
        print(f"Input direction: {self.input_direction}")

    def select(self, value: bool) -> None:
        pass

    def update_deadzone(self, deadzone: float) -> None:
        self.__square_deadzone = deadzone * deadzone

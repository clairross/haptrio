from controls.controllable import Controllable
from controls.controls import ControllerState


class Controller:
    targets: list[Controllable]
    is_enabled: bool

    def __init__(self):
        self.targets = []
        self.is_enabled = True

    def enable(self):
        self.is_enabled = True

    def disable(self):
        self.is_enabled = False

    def update(self):
        if not self.is_enabled:
            return

        for target in self.targets:
            target.control(self.get_state())

    def get_state(self) -> ControllerState:
        raise NotImplementedError

    def register_target(self, target: Controllable):
        self.targets.append(target)

    def deregister_target(self, target: Controllable):
        self.targets.remove(target)

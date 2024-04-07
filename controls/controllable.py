from controls.controls import ControllerState


class Controllable:
    def control(self, control_state: ControllerState) -> None:
        raise NotImplementedError

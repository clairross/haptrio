from py5 import Py5Vector as PVector


class ForceGenerator:
    def __init__(self):
        pass

    def get_current_force(self) -> PVector:
        raise NotImplementedError

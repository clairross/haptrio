from py5 import Py5Vector as PVector
from typing import cast
from physics.force_generator import ForceGenerator


class ForceManager:
    force_generators: list[ForceGenerator] = []

    def __init__(self):
        self.forces: list[ForceGenerator] = []
        self.force_registry = {}

    @staticmethod
    def add_force_generator(force_generator: ForceGenerator):
        ForceManager.force_generators.append(force_generator)

    @staticmethod
    def remove_force_generator(force_generator: ForceGenerator):
        ForceManager.force_generators.remove(force_generator)

    @staticmethod
    def get_current_force_sum() -> PVector:
        force_sum: PVector = PVector(0, 0)
        for force_generator in ForceManager.force_generators:
            force_sum = force_sum + force_generator.get_current_force()
        return force_sum

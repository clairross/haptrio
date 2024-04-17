class Vibration:
    current_index: int
    magnitudes: list[int]

    def __init__(self, magnitude_pattern: list[int]) -> None:
        self.current_index = 0
        self.magnitudes = magnitude_pattern

    def get_next_magnitude(self) -> int:
        magnitude = self.magnitudes[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.magnitudes)
        return (
            magnitude - 12
        )  # TODO: 12 is the middle so we range from -12 to 13 in magnitudes

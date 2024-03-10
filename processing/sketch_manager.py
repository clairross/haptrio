from py5 import Sketch


class SketchManager:
    __current_sketch: Sketch

    @staticmethod
    def get_current_sketch() -> Sketch:
        return SketchManager.__current_sketch

    @staticmethod
    def set_current_sketch(sketch: Sketch) -> None:
        SketchManager.__current_sketch = sketch

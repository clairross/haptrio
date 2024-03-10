from processing.sketch import Sketch
from processing.sketch_manager import SketchManager


def __main__():
    sketch = Sketch()
    SketchManager.set_current_sketch(sketch)
    sketch.run_sketch()


__main__()

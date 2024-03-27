from py5 import color, Py5Vector as PVector
from resources.resource_manager import ResourceManager, Resources
from interface.background import Background
from interface.xylophone import Xylophone
from shapes.rectangle import Rectangle
from world_map.world import WORLD_HALF_WIDTH, WORLD_PIXEL_HEIGHT


class Map:
    """The map of the world.  This class is responsible for drawing the map"""

    background: Background
    xylophone: Xylophone

    def __init__(self):
        resources: Resources = ResourceManager.get_resources()
        self.background = Background(resources.images.staff)
        self.xylophone = Xylophone(
            Rectangle(WORLD_HALF_WIDTH - (580 / 2), WORLD_PIXEL_HEIGHT - 247, 580, 247),
            num_keys=8,
            key_colors=[
                color("#Fd2828"),
                color("#F9893b"),
                color("#EEFB5D"),
                color("#61D729"),
                color("#51D2E3"),
                color("#2E2AED"),
                color("#B01B5A"),
            ],
            key_padding=8,
        )

        return

    def input(self, key: int):
        self.xylophone.play_key(key)

    def click(self, mouse_position: PVector):
        self.xylophone.click(mouse_position)

    def draw(self):
        self.background.draw()
        self.xylophone.draw()

    def update(self):
        return

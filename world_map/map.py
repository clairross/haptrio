from resources.resource_manager import ResourceManager, Resources
from interface.background import Background


class Map:
    """The map of the world.  This class is responsible for drawing the map"""

    background: Background

    def __init__(self):
        resources: Resources = ResourceManager.get_resources()
        self.background = Background(resources.images.staff)

        return

    def draw(self):
        self.background.draw()

    def update(self):
        # print("Map.update")
        return

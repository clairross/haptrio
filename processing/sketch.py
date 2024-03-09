import py5
from py5 import Sketch as PSketch, CORNER, Py5Vector as PVector
from system.operating_system import OperatingSystem
from processing.screen import BASE_FRAME_RATE, SCREEN_PIXEL_HEIGHT, SCREEN_PIXEL_WIDTH
from haply.haply import Haply
from world_map.map import Map
from player.player import Player
from scheduler.scheduler import Scheduler
from system.diagnostics import Diagnostics
from system.environment import Environment


class Sketch(PSketch):
    haply: Haply
    map: Map
    player: Player
    debug_mode: bool
    diagnostics: Diagnostics

    def settings(self):
        self.debug_mode = Environment.get("debug_mode")

        if self.debug_mode:
            self.diagnostics = Diagnostics()

        OperatingSystem().setup()
        self.size(SCREEN_PIXEL_WIDTH, SCREEN_PIXEL_HEIGHT)

    def setup(self):
        self.frame_rate(BASE_FRAME_RATE)
        self.haply = Haply()
        self.rect_mode(CORNER)
        self.map = Map()
        self.player = Player(PVector(0, 0))

        self.scheduler = Scheduler(1, self.update)
        self.scheduler.run()

    def update(self):
        print("Update")
        self.haply.update()
        self.map.update()

    def draw(self):
        print("Draw")
        if self.scheduler.is_running:
            return

        try:
            if self.debug_mode:
                self.diagnostics.draw()

            self.push_matrix()
            # Center 0,0
            self.translate(SCREEN_PIXEL_WIDTH, SCREEN_PIXEL_HEIGHT)
            self.map.draw()
            self.player.draw()
            self.pop_matrix()
        except Exception as e:
            print(e)

    def exiting(self):
        print("Exiting")

    def mousePressed(self):
        print("Mouse pressed")

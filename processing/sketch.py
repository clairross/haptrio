from py5 import Sketch as PSketch, CORNER, Py5Vector as PVector
from system.operating_system import OperatingSystem
from processing.screen import (
    BASE_FRAME_RATE,
    SCREEN_PIXEL_HEIGHT,
    SCREEN_PIXEL_WIDTH,
    SCREEN_CENTER,
)
from haply.haply import Haply
from world_map.map import Map
from player.player import Player
from scheduler.scheduler import Scheduler
from system.diagnostics import Diagnostics
from system.environment import Environment, ROOT_DIRECTORY
from random import randint


class Sketch(PSketch):
    haply: Haply
    map: Map
    player: Player
    updateScheduler: Scheduler[None]
    debug_mode: bool
    diagnostics: Diagnostics

    def settings(self):
        self.debug_mode = Environment.get("debug_mode")

        if self.debug_mode:
            self.diagnostics = Diagnostics()

        OperatingSystem().setup()
        self.size(SCREEN_PIXEL_WIDTH, SCREEN_PIXEL_HEIGHT)

    def setup(self):

        self.window_title("HapTrio")
        self.get_surface().set_icon(
            self.load_image(f"{ROOT_DIRECTORY}/data/images/icon.png")
        )
        self.frame_rate(BASE_FRAME_RATE)
        self.haply = Haply()
        self.rect_mode(CORNER)
        self.map = Map()
        self.player = Player(SCREEN_CENTER)

        self.updateScheduler = Scheduler(1, self.update)
        self.updateScheduler.run()

    def update(self):
        # print("Update")

        if self.haply.is_active:
            self.haply.update()

        self.player.update(PVector(0, 0))
        self.map.update()

    def draw(self):
        if self.updateScheduler.is_running:
            return

        print("Draw")
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
            print(e.with_traceback)
            raise e

    def exiting(self):
        print("Exiting")

    def mouse_pressed(self):
        print("Mouse pressed")
        self.fill(randint(1, 255), randint(1, 255), randint(1, 255))
        self.square(self.mouse_x, self.mouse_y, 10)

from py5 import Sketch as PSketch, CORNER, Py5Vector as PVector, color
from system.operating_system import OperatingSystem
from haply.haply import Haply
from world_map.map import Map
from player.player import Player
from scheduler.scheduler import Scheduler
from system.diagnostics import Diagnostics
from system.environment import Environment, ROOT_DIRECTORY
from random import randint
from shapes.circle import Circle
from shapes.line import Line
from resources.resource_manager import ResourceManager, Resources
from processing.screen import Screen


class Sketch(PSketch):
    haply: Haply
    map: Map
    player: Player
    updateScheduler: Scheduler[None]
    debug_mode: bool
    diagnostics: Diagnostics
    screen: Screen

    def settings(self):
        self.debug_mode = Environment.get("debug_mode")

        if self.debug_mode:
            self.diagnostics = Diagnostics()

        OperatingSystem().setup()
        self.screen = Screen()
        self.screen.subscribe_to_window_changed(self.window_size_changed)
        self.size(self.screen.width, self.screen.height)

    def setup(self):

        self.window_title("HapTrio")
        resources: Resources = ResourceManager.get_resources()
        self.screen.set_window_icon(f"{ROOT_DIRECTORY}/{resources.app_icon}")
        self.screen.set_window_resizable(True)
        self.frame_rate(self.screen.frame_rate)
        self.rect_mode(CORNER)
        self.map = Map()
        self.haply = Haply()
        self.player = Player(self.screen.center)

        self.updateScheduler = Scheduler(1, self.update)
        self.updateScheduler.run()

    def update(self):
        # print("Update")
        self.screen.update()

        if self.haply.is_active:
            self.haply.update()

        self.map.update()
        self.player.update(PVector(0, 0))

    def draw(self):
        if self.updateScheduler.is_running:
            return

        # print("Draw")
        try:
            if self.debug_mode:
                self.diagnostics.draw()

            # Center 0,0
            # self.translate(SCREEN_PIXEL_WIDTH, SCREEN_PIXEL_HEIGHT)
            self.map.draw()
            self.player.draw()
        except Exception as e:
            print(e.with_traceback)
            raise e

    def exiting(self):
        print("Exiting")

    def mouse_pressed(self):
        print("Mouse pressed")
        mouse_position = PVector(self.mouse_x, self.mouse_y)
        c11 = Circle(mouse_position, 10, fill_color=color(255, 0, 0))
        c11.draw()
        self.fill(randint(1, 255), randint(1, 255), randint(1, 255))
        self.square(self.mouse_x, self.mouse_y, 10)
        l12 = Line(mouse_position, PVector.__add__(mouse_position, PVector(100, 100)))
        l12.draw()

        print(
            f"Mouse pressed at {mouse_position}, line = {l12.shape}, circle = {c11.shape}"
        )

    def window_size_changed(self, width: int, height: int):
        print(f"Window size changed to {width} x {height}")

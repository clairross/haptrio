from py5 import (
    Sketch as PSketch,
    CORNER,
    Py5Vector as PVector,
    color,
    Py5KeyEvent as KeyEvent,
    Py5MouseEvent as MouseEvent,
)
from system.operating_system import OperatingSystem
from haply.haply import Haply
from world_map.scene import Scene
from player.player import Player
from scheduler.scheduler import Scheduler
from system.diagnostics import Diagnostics
from system.environment import Environment, ROOT_DIRECTORY
from random import randint
from shapes.circle import Circle
from shapes.line import Line
from resources.resource_manager import ResourceManager, Resources
from processing.screen import Screen
from pygame.mixer import init as InitializeAudioMixer


class Sketch(PSketch):
    haply: Haply
    scene: Scene
    player: Player
    updateScheduler: Scheduler[None]
    debug_mode: bool
    diagnostics: Diagnostics
    screen: Screen

    def settings(self):
        self.debug_mode = Environment.get().debug_mode

        if self.debug_mode:
            self.diagnostics = Diagnostics()

        OperatingSystem().setup()
        self.screen = Screen()
        self.screen.subscribe_to_window_changed(self.window_size_changed)
        self.size(self.screen.width, self.screen.height)

    def setup(self):

        self.window_title("HapTrio")
        resources: Resources = ResourceManager.get()
        self.screen.set_window_icon(f"{ROOT_DIRECTORY}/{resources.app_icon}")
        self.screen.set_window_resizable(True)
        self.frame_rate(self.screen.frame_rate)
        self.rect_mode(CORNER)
        InitializeAudioMixer()
        self.scene = Scene()
        self.haply = Haply()
        self.player = Player(self.screen.center)
        self.haply.register_target(self.player)

        self.updateScheduler = Scheduler(1, self.update)
        self.updateScheduler.run()

    def update(self):
        # print("Update")
        self.screen.update()

        if self.haply.is_enabled:
            self.haply.update()

        self.scene.update()
        self.player.update()

    def draw(self):
        if self.updateScheduler.is_running:
            return

        # print("Draw")
        try:
            if self.debug_mode:
                self.diagnostics.draw()

            # Center 0,0
            # self.translate(SCREEN_PIXEL_WIDTH, SCREEN_PIXEL_HEIGHT)
            self.scene.draw()
            self.player.draw()
        except Exception as e:
            print(e.with_traceback)
            raise e

    def exiting(self):
        print("Exiting")

    def mouse_pressed(self):
        print("Mouse pressed")
        mouse_position = PVector(self.mouse_x, self.mouse_y)
        print(f"Mouse pressed at {mouse_position}")
        self.scene.click(mouse_position)

    def key_pressed(self):
        print(f"Key pressed: {self.key}")
        self.map.input(int(self.key))

    def window_size_changed(self, width: int, height: int):
        print(f"Window size changed to {width} x {height}")

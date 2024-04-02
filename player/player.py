from py5 import Py5Vector as PVector, Sketch as PSketch, ELLIPSE, color
from processing.sketch_manager import SketchManager
from shapes.circle import Circle
from system.environment import Environment
from controls.controllable import Controllable
from controls.controls import ControllerState


class Player(Controllable):
    position: PVector
    speed_multiplier: float = 50
    player_size: float = 50
    shell_size: float = player_size * 1.4
    max_shell_penetration: float = 12
    k_spring_shell: float = 0.5
    b_damping_shell: float = 2.5
    c_drag_shell: float = 1
    mass: float = 1
    cross_section_area: float = 1
    is_moving_outward: bool
    sketch: PSketch
    player_ball: Circle
    shell: Circle
    velocity: PVector
    shell_penetration_distance: float
    __old_position: PVector

    def __init__(self, initial_position: PVector):
        print(f"Creating player at {initial_position}")
        self.sketch = SketchManager.get_current_sketch()

        self.is_moving_outward = False
        self.__old_position = initial_position
        self.position = initial_position
        self.player_ball = Circle(initial_position, self.player_size, color("#EEEEEE"))
        self.shell = Circle(initial_position, self.shell_size, color("#222222"))
        self.shell_penetration_distance = 0
        self.shell_penetration = PVector(0, 0)
        self.velocity = PVector(0, 0)
        print(f"Player created at {self.position}")
        # self.shell = Circle(self.position, self.shellSize, py5.color(150))

    def update(self):
        old_shell_penetration_distance = self.shell_penetration_distance
        # self.move(position_offset)
        self.shell_penetration_distance = self.__get_shell_penetration_magnitude()
        self.is_moving_outward = (
            self.shell_penetration_distance > old_shell_penetration_distance
        )

        self.velocity = (
            self.position - self.__old_position
        )  # / (GameTime.ElapsedGameTime.toNanos() / 1000000))
        self.__old_position = self.position.copy

        print(f"Player velocity: {self.velocity}")

        self.player_ball.translate(self.velocity)
        self.shell.translate(self.velocity)

        if Environment.get().debug_mode:
            self.sketch.push_matrix()
            self.sketch.line(
                self.position.x, self.position.y, old_position.x, old_position.y
            )
            self.sketch.pop_matrix()

    def draw(self):
        # print(f"Drawing player at {self.position}")
        self.sketch.push_matrix()
        # self.sketch.translate(self.position.x, self.position.y)
        self.shell.draw()
        self.player_ball.draw()
        self.sketch.pop_matrix()

    def control(self, control_state: ControllerState):
        movement = PVector(control_state.movement[0], control_state.movement[1])

        self.move(movement)

    def get_shell_penetration_resistance_force(self) -> PVector:
        shell_penetration_force = (
            self.position.copy.set_mag(self.shell_penetration_distance)
            * self.k_spring_shell
        )

        if self.is_moving_outward:
            shell_penetration_force += self.velocity * self.b_damping_shell

        return shell_penetration_force * -1

    def move(self, direction: PVector) -> None:
        print(f"Moving player by {direction}")
        self.position = self.position + (direction * self.speed_multiplier)

    def __get_shell_penetration_magnitude(self):
        shell_start_distance = (self.shell_size - self.player_size) / 2
        position_magnitude = self.position.mag

        if position_magnitude > shell_start_distance:
            return position_magnitude - shell_start_distance

        return 0

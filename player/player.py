import py5
from py5 import Py5Vector as PVector, get_current_sketch, create_shape

sketch = get_current_sketch()
# from shapes.circle import Circle
from system.environment import DEBUG_MODE


class Player:
    position: PVector
    speed_multiplier: float = 450
    player_size: float = 50
    shell_size: float = player_size * 1.2
    max_shell_penetration: float = 12
    k_spring_shell: float = 0.5
    b_damping_shell: float = 2.5
    c_drag_shell: float = 1
    mass: float = 1
    cross_section_area: float = 1
    is_moving_into_wall: bool

    def __init__(self, initial_position: PVector):
        print(f"Creating player at {initial_position}")
        self.playerBall = create_shape(
            py5.ELLIPSE,
            initial_position.x,
            initial_position.y,
            self.player_size,
            self.player_size,
        )
        self.playerBall.set_stroke(py5.color(10))
        self.playerBall.stroke_weight(10)

        self.player_shell = py5.create_shape(
            py5.ELLIPSE,
            initial_position.x,
            initial_position.y,
            self.shell_size,
            self.shell_size,
        )
        self.player_shell.set_stroke(py5.color(150))
        self.player_shell.stroke_weight(15)
        self.is_moving_into_wall = False
        self.position = initial_position
        self.velocity = PVector(0, 0)
        self.wall_penetration = PVector(0, 0)
        self.shell_penetration_distance = 0
        self.shell_penetration = PVector(0, 0)
        # self.shell = Circle(self.position, self.shellSize, py5.color(150))

    def update(self, position_offset: PVector):
        old_position = self.position
        old_shell_penetration_distance = self.shell_penetration_distance
        self.move(position_offset)
        self.update_shell_penetration()

        self.velocity = (
            self.position - old_position
        )  # / (GameTime.ElapsedGameTime.toNanos() / 1000000))
        self.is_moving_into_wall = (
            self.shell_penetration_distance > old_shell_penetration_distance
        )

        if DEBUG_MODE:
            sketch.push_matrix()
            sketch.line(
                self.position.x, self.position.y, old_position.x, old_position.y
            )
            sketch.pop_matrix()

    def draw(self):
        sketch.push_matrix()
        sketch.shape(self.player_shell)
        sketch.push_matrix()
        sketch.translate(self.position.x, self.position.y)
        sketch.shape(self.playerBall)
        sketch.pop_matrix()
        sketch.pop_matrix()

    def get_shell_penetration_resistance_force(self):
        shell_penetration_force = self.shell_penetration * self.k_spring_shell

        if self.is_moving_into_wall:
            shell_penetration_force += self.velocity * self.b_damping_shell

        return shell_penetration_force * -1

    def get_wall_force(self):
        return self.wall_penetration

    def get_shell(self):
        return self.shell

    def move(self, direction: PVector) -> None:
        self.position = direction * self.speed_multiplier

    def update_shell_penetration(self):
        shell_start_distance = (self.shell_size - self.player_size) / 2
        position_magnitude = self.position.mag

        if position_magnitude > shell_start_distance:
            self.shell_penetration_distance = position_magnitude - shell_start_distance
            self.shell_penetration = self.position.set_mag(
                self.shell_penetration_distance
            )
        else:
            self.shell_penetration = PVector(0, 0)
            self.shell_penetration_distance = 0

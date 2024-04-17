"""This module contains the Haply class, which is used to control the Haply device."""

from typing import Final, Callable
from py5 import Py5Vector as PVector
from controls.controls import ControllerState
from system.ports import Ports
from haply.types import Board, Device, Pantograph, COUNTER_CLOCKWISE
from system.environment import Environment
from controls.controller import Controller
from physics.force_manager import ForceManager


class Haply(Controller):
    HARDWARE_VERSION: Final[int] = (
        3  # 2 for the metallic plate device, 3 for the newer plastic device
    )
    DEVICE_ID: Final[int] = 5
    BAUD_RATE: Final[int] = 0
    TICKS_PER_ROTATION: Final[int] = 4096
    DEVICE_ORIGIN_CORRECTION: Final[tuple[float, float]] = (-0.01902388, 0.03573548)
    angles: PVector
    torques: PVector
    port: str
    board: Board
    device: Device
    updating: bool = False
    device_position: PVector

    def __init__(self, com_port: str = Environment.get().port):
        """Initialize the Haply device."""
        super().__init__()
        ports = Ports()

        if not ports.has_port(com_port):
            self.port = ports.select_port()
        else:
            self.port = Environment.get().port

        if self.port == "":
            print(
                "No available port, no Haply device will be used. \
However, you can continue using the program without it."
            )
            return

        print("Starting the application!")
        self.board: Board = Board(self.port, self.port, self.BAUD_RATE)
        self.device: Device = Device(self.DEVICE_ID, self.board)
        pantograph = Pantograph(self.HARDWARE_VERSION)
        # self.device.add_analog_sensor("A2")
        self.device.set_mechanism(pantograph)

        self.device.add_actuator(1, COUNTER_CLOCKWISE, 2)
        self.device.add_actuator(2, COUNTER_CLOCKWISE, 1)

        if Environment.get().flip_y_haply:
            self.device.add_encoder(
                1, COUNTER_CLOCKWISE, 168, self.TICKS_PER_ROTATION, 1
            )
            self.device.add_encoder(
                2, COUNTER_CLOCKWISE, 12, self.TICKS_PER_ROTATION, 2
            )
        else:
            self.device.add_encoder(
                1, COUNTER_CLOCKWISE, 168, self.TICKS_PER_ROTATION, 2
            )
            self.device.add_encoder(
                2, COUNTER_CLOCKWISE, 12, self.TICKS_PER_ROTATION, 1
            )

        self.device.device_set_parameters()
        self.device_position = PVector(0, 0)
        print("Haply device is active!")

    def update(self):
        """Update the Haply, read data from the device and set the torques."""
        super().update()

        if self.board.data_available():
            self.updating = True
            self.device.device_read_data()
            motorAngle = self.device.get_device_angles()
            device_position = self.device.get_device_position(motorAngle)
            self.device_position = PVector(
                -device_position[0] - self.DEVICE_ORIGIN_CORRECTION[0],
                device_position[1] - self.DEVICE_ORIGIN_CORRECTION[1],
            )
            # print(f"Device position: {device_position_vector}")

        self.device.set_device_torques(ForceManager.get_current_force_sum().tolist())
        self.device.device_write_torques()
        self.updating = False

    def get_state(self) -> ControllerState:
        """Get the input from the Haply device."""

        return ControllerState(
            (self.device_position.x, self.device_position.y), False, False
        )

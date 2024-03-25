"""This module contains the Haply class, which is used to control the Haply device."""

from typing import Final
from py5 import Py5Vector as PVector
from system.ports import Ports
from haply.types import Board, Device, Pantograph, COUNTER_CLOCKWISE
from system.environment import DEVICE_PORT


class Haply:
    HARDWARE_VERSION: Final[int] = (
        3  # 2 for the metallic plate device, 3 for the newer plastic device
    )
    DEVICE_ID: Final[int] = 5
    BAUD_RATE: Final[int] = 0
    TICKS_PER_ROTATION: Final[int] = 4096
    DEVICE_ORIGIN: Final[PVector] = PVector(0, 0)
    angles: PVector
    torques: PVector
    port: str
    board: Board
    device: Device
    updating: bool = False
    current_force: PVector = PVector(0, 0)
    is_active: bool = False

    def __init__(self, com_port: str = DEVICE_PORT):
        ports = Ports()

        if not ports.has_port(com_port):
            self.port = ports.select_port()
        else:
            self.port = DEVICE_PORT

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
        self.device.add_encoder(1, COUNTER_CLOCKWISE, 168, self.TICKS_PER_ROTATION, 1)
        self.device.add_encoder(2, COUNTER_CLOCKWISE, 12, self.TICKS_PER_ROTATION, 2)
        self.device.device_set_parameters()
        self.is_active = True
        print("Haply device is active!")

    def update(self):
        """Update the Haply, read data from the device and set the torques."""
        if self.board.data_available():
            self.updating = True
            self.device.device_read_data()
            motorAngle = self.device.get_device_angles()
            device_position = self.device.get_device_position(motorAngle)
            print("Device position: " + str(device_position))

        self.device.set_device_torques(self.current_force.tolist())
        self.device.device_write_torques()
        self.updating = False

    def set_forces(self, force: PVector):
        """Set the forces to apply to the Haply."""
        self.current_force = force

"""This module defines the types used in the Haply library."""

from typing import List, Protocol, Final


CLOCKWISE: Final[int] = 0
COUNTER_CLOCKWISE: Final[int] = 1


class Actuator(Protocol):
    """The Actuator class represents a component of a Mechanism.
    For example, it is a motor that can be used to move a mechanism.
    """

    def __init__(self, actuator: int, direction: int, port: int):
        """Create an Actuator

        Args:
            actuator (int, optional): actuator index. Defaults to 0.
            direction (int, optional): direction. Defaults to 0.
            port (int, optional): motor port position for actuator. Defaults to 0.
        """
        raise NotImplementedError

    def set_actuator(self, actuator: int) -> None:
        """Set actuator index parameter of sensor

        Args:
            actuator ([type]): [index]
        """

    def set_direction(self, direction: int) -> None:
        """Set actuator rotation direction

        Args:
            direction ([type]): direction of rotation
        """

    def set_port(self, port: int) -> None:
        """sets motor port position

        Args:
            port ([type]): port index
        """

    def set_torque(self, torque: float) -> None:
        """sets torque variable to the given torque value

        Args:
            torque ([type]): new torque value for update
        """

    def get_actuator(self) -> int:
        """get actuator index

        Returns:
            [type]: actuator index
        """
        raise NotImplementedError

    def get_direction(self) -> int:
        """get actuator rotation direction

        Returns:
            [type]: rotation direction
        """
        raise NotImplementedError

    def get_port(self) -> int:
        """get motor port position

        Returns:
            [type]: port index
        """
        raise NotImplementedError

    def get_torque(self) -> float:
        """get torque value

        Returns:
            [type]: torque value
        """
        raise NotImplementedError


class Board(Protocol):
    """Define Board system

    Returns:
        [type]: [description]
    """

    def __init__(self, app: str, port: str, baud: int):
        """Initialise Bard

        Args:
            app (string): name of the app
            port (string): com port
            baud (int): rate
        """
        raise NotImplementedError

    def floatToBits(self, f: float) -> int:
        """Convert float to bits"""
        raise NotImplementedError

    def bitsToFloat(self, b: int) -> float:
        """Convert bits to float"""
        raise NotImplementedError

    def float_to_bytes(self, float_data: float) -> bytearray:
        """Convert float to bytes"""
        raise NotImplementedError

    def bytes_to_float(self, data: bytes) -> float:
        """Convert bytes to float"""
        raise NotImplementedError

    def transmit(
        self,
        communicationType: int,
        deviceID: int,
        bData: List[int],
        fData: List[float],
    ) -> None:
        """Transmit data to device"""
        raise NotImplementedError

    def receive(
        self, communicationType: int, deviceID: int, expected: int
    ) -> List[float]:
        """Receive data from device"""
        raise NotImplementedError

    def data_available(self) -> bool:
        """Check if data is available"""
        raise NotImplementedError


class Mechanisms(Protocol):
    """Mechanisms class to define the mechanism"""

    def forwardKinematics(self, angles: List[float]) -> None:
        raise NotImplementedError

    def torqueCalculation(self, force: List[float]) -> None:
        raise NotImplementedError

    def forceCalculation(self) -> None:
        raise NotImplementedError

    def positionControl(self) -> None:
        raise NotImplementedError

    def inverseKinematics(self) -> None:
        raise NotImplementedError

    def set_mechanism_parameters(self, parameters: List[float]) -> None:
        raise NotImplementedError

    def set_sensor_data(self, data: List[float]) -> None:
        raise NotImplementedError

    def get_coordinate(self) -> List[float]:
        raise NotImplementedError

    def get_torque(self) -> List[float]:
        raise NotImplementedError

    def get_angle(self) -> List[float]:
        raise NotImplementedError


class Pwm(Protocol):
    """Pwm class to define the pulse width modulation"""

    def __init__(self, pin: int, pulsewidth: float):
        """Create a Pwm object"""
        raise NotImplementedError

    def set_pin(self, pin: int) -> None:
        raise NotImplementedError

    def set_pulse(self, percent: float) -> None:
        raise NotImplementedError

    def get_pin(self) -> int:
        raise NotImplementedError

    def get_value(self) -> int:
        raise NotImplementedError

    def get_pulse(self) -> float:
        raise NotImplementedError


class Sensor(Protocol):
    def __init__(
        self, encoder: int, direction: int, offset: int, resolution: int, port: int
    ):
        raise NotImplementedError

    def set_encoder(self, encoder: int) -> None:
        raise NotImplementedError

    def set_direction(self, direction: int) -> None:
        raise NotImplementedError

    def set_offset(self, offset: int) -> None:
        raise NotImplementedError

    def set_resolution(self, resolution: int) -> None:
        raise NotImplementedError

    def set_port(self, port: int) -> None:
        raise NotImplementedError

    def set_value(self, value: int) -> None:
        raise NotImplementedError

    def get_encoder(self) -> int:
        raise NotImplementedError

    def get_direction(self) -> int:
        raise NotImplementedError

    def get_offset(self) -> int:
        raise NotImplementedError

    def get_resolution(self) -> int:
        raise NotImplementedError

    def get_port(self) -> int:
        raise NotImplementedError

    def get_value(self) -> int:
        raise NotImplementedError


class Device:
    def __init__(self, deviceID: int, deviceLink: Board):
        raise NotImplementedError

    def add_actuator(self, actuator: int, rotation: int, port: int) -> None:
        """Add an actuator to the device"""
        raise NotImplementedError

    def add_encoder(
        self, encoder: int, rotation: int, offset: int, resolution: int, port: int
    ) -> None:
        raise NotImplementedError

    def add_analog_sensor(self, pin: str) -> None:
        raise NotImplementedError

    def add_pwm_pin(self, pin: int) -> None:
        raise NotImplementedError

    def set_mechanism(self, mechanism: Mechanisms) -> None:
        raise NotImplementedError

    def device_set_parameters(self) -> None:
        raise NotImplementedError

    def device_read_data(self) -> None:
        raise NotImplementedError

    def device_read_request(self) -> None:
        raise NotImplementedError

    def device_write_torques(self) -> None:
        raise NotImplementedError

    def set_pwm_pulse(self, pin: int, pulse: float) -> None:
        raise NotImplementedError

    def get_pwm_pulse(self, pin: int) -> float:
        raise NotImplementedError

    def get_device_angles(self) -> List[float]:
        raise NotImplementedError

    def get_sensor_data(self) -> List[float]:
        raise NotImplementedError

    def get_device_position(self, angles: List[float]) -> List[float]:
        raise NotImplementedError

    def set_device_torques(self, forces: List[float]) -> List[float]:
        raise NotImplementedError


class Pantograph(Mechanisms):
    def __init__(self, version: int):
        raise NotImplementedError

    def forwardKinematics(self, angles: List[float]) -> None:
        raise NotImplementedError

    def torqueCalculation(self, force: List[float]) -> None:
        raise NotImplementedError

    def op_velocityCalculation(self, q: List[float]) -> List[float]:
        raise NotImplementedError

    def forceCalculation(self) -> None:
        raise NotImplementedError

    def positionControl(self) -> None:
        raise NotImplementedError

    def inverseKinematics(self) -> None:
        raise NotImplementedError

    def set_mechanism_parameters(self, parameters: List[float]) -> None:
        raise NotImplementedError

    def set_sensor_data(self, data: List[float]) -> None:
        raise NotImplementedError

    def get_coordinate(self) -> List[float]:
        raise NotImplementedError

    def get_torque(self) -> List[float]:
        raise NotImplementedError

    def get_angle(self) -> List[float]:
        raise NotImplementedError

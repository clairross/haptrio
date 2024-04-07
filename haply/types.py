"""This module defines the types used in the Haply library.

The types beign replaced are from here:
https://gitlab.com/Haply/2diy/pyhapi/-/blob/master/src/HaplyHAPI.py?ref_type=heads
"""

import sys
import time
from typing import List, Final
from HaplyHAPI import (
    Actuator as HActuator,
    Device as HDevice,
    Mechanisms as HMechanicsms,
    Sensor as HSensor,
    Board as HBoard,
    Pantograph as HPantograph,
    Pwm as HPwm,
)

CLOCKWISE: Final[int] = 0
COUNTER_CLOCKWISE: Final[int] = 1


class Actuator(HActuator):
    """The Actuator class represents a component of a Mechanism.
    For example, it is a motor that can be used to move a mechanism.
    """

    def __init__(self, actuator: int = 0, direction: int = 0, port: int = 0):
        """Create an Actuator

        Args:
            actuator (int, optional): actuator index. Defaults to 0.
            direction (int, optional): direction. Defaults to 0.
            port (int, optional): motor port position for actuator. Defaults to 0.
        """
        super().__init__(actuator, direction, port)

    def set_actuator(self, actuator: int) -> None:
        """Set actuator index parameter of sensor

        Args:
            actuator ([type]): [index]
        """
        super().set_actuator(actuator)

    def set_direction(self, direction: int) -> None:
        """Set actuator rotation direction

        Args:
            direction ([type]): direction of rotation
        """
        super().set_direction(direction)

    def set_port(self, port: int) -> None:
        """sets motor port position

        Args:
            port ([type]): port index
        """
        super().set_port(port)

    def set_torque(self, torque: float) -> None:
        """sets torque variable to the given torque value

        Args:
            torque ([type]): new torque value for update
        """
        super().set_torque(torque)

    def get_actuator(self) -> int:
        """get actuator index

        Returns:
            [type]: actuator index
        """
        return super().get_actuator()

    def get_direction(self) -> int:
        """get actuator rotation direction

        Returns:
            [type]: rotation direction
        """
        return super().get_direction()

    def get_port(self) -> int:
        """get motor port position

        Returns:
            [type]: port index
        """
        return super().get_port()

    def get_torque(self) -> float:
        """get torque value

        Returns:
            [type]: torque value
        """
        return super().get_torque()


class Board(HBoard):
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
        super().__init__(app, port, baud)

    def floatToBits(self, f: float) -> int:
        """Convert float to bits"""
        return super().floatToBits(f)

    def bitsToFloat(self, b: int) -> float:
        """Convert bits to float"""
        return super().bitsToFloat(b)

    def float_to_bytes(self, float_data: float) -> bytearray:
        """Convert float to bytes"""
        return super().float_to_bytes(float_data)

    def bytes_to_float(self, data: bytes) -> float:
        """Convert bytes to float"""
        return super().bytes_to_float(data)

    def transmit(
        self,
        communicationType: int,
        deviceID: int,
        bData: List[int],
        fData: List[float],
    ) -> None:
        """Transmit data to device"""
        super().transmit(communicationType, deviceID, bData, fData)

    def receive(
        self, communicationType: int, deviceID: int, expected: int
    ) -> List[float]:
        """Receive data from device"""
        return super().receive(communicationType, deviceID, expected)
        # # expected = expected - 1  # REMOVE
        # inData = bytearray(1 + 4 * expected)
        # data = [None] * expected
        # # print("Receiving data from the device.")
        # inData = self._Board__port.read(1 + 4 * expected + 1)
        # # print("Data received from the device, inData: " + str(inData))
        # if inData[0] != deviceID:
        #     sys.stderr.write("Error, another device expects this data!\n")
        # buf = inData[1 : expected * 4 + 1]
        # for i in range(0, expected):
        #     data[i] = self.bytes_to_float(buf[i * 4 : i * 4 + 4])
        # # data = struct.unpack('!'+str(expected)+'f', buf)
        # # print(expected)
        # # print(data)
        # return data

    def data_available(self) -> bool:
        """Check if data is available"""
        return super().data_available()


class Mechanisms(HMechanicsms):
    """Mechanisms class to define the mechanism"""

    def forwardKinematics(self, angles: List[float]) -> None:
        super().forwardKinematics(angles)

    def torqueCalculation(self, force: List[float]) -> None:
        super().torqueCalculation(force)

    def forceCalculation(self) -> None:
        super().forceCalculation()

    def positionControl(self) -> None:
        super().positionControl()

    def inverseKinematics(self) -> None:
        super().inverseKinematics()

    def set_mechanism_parameters(self, parameters: List[float]) -> None:
        super().set_mechanism_parameters(parameters)

    def set_sensor_data(self, data: List[float]) -> None:
        super().set_sensor_data(data)

    def get_coordinate(self) -> List[float]:
        return super().get_coordinate()

    def get_torque(self) -> List[float]:
        return super().get_torque()

    def get_angle(self) -> List[float]:
        return super().get_angle()


class Pwm(HPwm):
    """Pwm class to define the pulse width modulation"""

    def __init__(self, pin: int = 0, pulsewidth: float = 0):
        """Create a Pwm object"""
        super().__init__(pin, pulsewidth)

    def set_pin(self, pin: int) -> None:
        super().set_pin(pin)

    def set_pulse(self, percent: float) -> None:
        super().set_pulse(percent)

    def get_pin(self) -> int:
        return super().get_pin()

    def get_value(self) -> int:
        return super().get_value()

    def get_pulse(self) -> float:
        return super().get_pulse()


class Sensor(HSensor):
    def __init__(
        self,
        encoder: int = 0,
        direction: int = 0,
        offset: int = 0,
        resolution: int = 0,
        port: int = 0,
    ):
        super().__init__(encoder, direction, offset, resolution, port)

    def set_encoder(self, encoder: int) -> None:
        super().set_encoder(encoder)

    def set_direction(self, direction: int) -> None:
        super().set_direction(direction)

    def set_offset(self, offset: int) -> None:
        super().set_offset(offset)

    def set_resolution(self, resolution: int) -> None:
        super().set_resolution(resolution)

    def set_port(self, port: int) -> None:
        super().set_port(port)

    def set_value(self, value: int) -> None:
        super().set_value(value)

    def get_encoder(self) -> int:
        return super().get_encoder()

    def get_direction(self) -> int:
        return super().get_direction()

    def get_offset(self) -> int:
        return super().get_offset()

    def get_resolution(self) -> int:
        return super().get_resolution()

    def get_port(self) -> int:
        return super().get_port()

    def get_value(self) -> int:
        return super().get_value()


class Device(HDevice):
    __sensorsActive: int
    __sensors: List[Sensor]

    def __init__(self, deviceID: int, deviceLink: Board):
        super().__init__(deviceID, deviceLink)
        self.vibration_active = False

    def add_actuator(self, actuator: int, rotation: int, port: int) -> None:
        """Add an actuator to the device"""
        super().add_actuator(actuator, rotation, port)

    def add_encoder(
        self, encoder: int, rotation: int, offset: int, resolution: int, port: int
    ) -> None:
        """Add an encoder to the device"""
        super().add_encoder(encoder, rotation, offset, resolution, port)

    def add_analog_sensor(self, pin: str) -> None:
        """Add an analog sensor to the device."""
        # self.device.add_analog_sensor(pin)

        print("Adding analog sensor to the device.")
        print("Pin: " + pin)
        error = False
        port = pin[0]
        number = pin[1:]
        value = int(number)
        value = value + 54

        for i in range(self._Device__sensorsActive):
            if value == self._Device__sensors[i].get_port():
                sys.stderr.write(
                    "error: Analog pin A" + (value - 54) + " has already been set"
                )
                error = True

        if port != "A" or value < 54 or value > 65:
            sys.stderr.write("error: outside analog pin range")
            error = True

        if not error:
            temp = self._Device__sensors
            temp.insert(self._Device__sensorsActive, Sensor())
            # temp[self._Device__sensorsActive] = Sensor()
            temp[self._Device__sensorsActive].set_port(value)
            self._Device__sensors = temp
            self._Device__sensorsActive += 1

    def add_pwm_pin(self, pin: int) -> None:
        """Add a pwm pin to the device"""
        super().add_pwm_pin(pin)

    def set_mechanism(self, mechanism: Mechanisms) -> None:
        """Set the mechanism for the device"""
        super().set_mechanism(mechanism)

    def device_set_parameters(self) -> None:
        """Set the device parameters"""
        super().device_set_parameters()

    def device_read_data(self) -> None:
        # print("Reading data from the device.")
        self._Device__communicationType = 2
        data_count = 0
        device_data = self._Device__deviceLink.receive(
            self._Device__communicationType,
            self._Device__deviceID,
            self._Device__sensorsActive + self._Device__encodersActive,
        )

        for i in range(self._Device__sensorsActive):
            self._Device__sensors[i].set_value(device_data[data_count])
            data_count += 1

        for i in range(len(self._Device__encoderPositions)):
            if self._Device__encoderPositions[i] > 0:
                self._Device__encoders[self._Device__encoderPositions[i] - 1].set_value(
                    device_data[data_count]
                )
                data_count += 1

    def device_read_request(self) -> None:
        """Request data from the device"""
        super().device_read_request()

    def device_write_torques(self) -> None:
        """Write torques to the device"""
        super().device_write_torques()

    def set_pwm_pulse(self, pin: int, pulse: float) -> None:
        """Set the pulse width modulation pulse"""
        super().set_pwm_pulse(pin, pulse)

    def get_pwm_pulse(self, pin: int) -> float:
        """Get the pulse width modulation pulse"""
        return super().get_pwm_pulse(pin)

    def get_device_angles(self) -> List[float]:
        """Get the device angles"""
        return super().get_device_angles()

    def get_sensor_data(self) -> List[float]:
        """Get the sensor data"""
        return super().get_sensor_data()

    def get_device_position(self, angles: List[float]) -> List[float]:
        """Get the device position"""
        return super().get_device_position(angles)

    def set_device_torques(self, forces: List[float]) -> List[float]:
        """Set the device torques"""
        return super().set_device_torques(forces)


class Pantograph(HPantograph):
    def __init__(self, version: int = 2):
        super().__init__(version)

    def forwardKinematics(self, angles: List[float]) -> None:
        super().forwardKinematics(angles)

    def torqueCalculation(self, force: List[float]) -> None:
        super().torqueCalculation(force)

    def op_velocityCalculation(self, q: List[float]) -> List[float]:
        return super().op_velocityCalculation(q)

    def forceCalculation(self) -> None:
        super().forceCalculation()

    def positionControl(self) -> None:
        super().positionControl()

    def inverseKinematics(self) -> None:
        super().inverseKinematics()

    def set_mechanism_parameters(self, parameters: List[float]) -> None:
        super().set_mechanism_parameters(parameters)

    def set_sensor_data(self, data: List[float]) -> None:
        super().set_sensor_data(data)

    def get_coordinate(self) -> List[float]:
        return super().get_coordinate()

    def get_torque(self) -> List[float]:
        return super().get_torque()

    def get_angle(self) -> List[float]:
        return super().get_angle()

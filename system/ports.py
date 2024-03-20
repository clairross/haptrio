"""Module to handle the available COM ports."""

from serial.tools.list_ports import comports


class Ports:
    """Class to handle the available COM ports."""

    available_com_ports: dict[int, str]
    selected_port: int

    def __init__(self):
        self.available_com_ports = {}
        self.selected_port = -1
        self.update_available_ports()

    def select_port(self) -> str:
        """Select the COM port if there are any."""
        self.update_available_ports()

        if len(self.available_com_ports) == 0:
            print("No COM ports available. Please connect a device and try again.")
            return ""

        print("Select the available COM port you'd like to use:")
        for i, port in self.available_com_ports.items():
            print(str(i) + ": " + port)
        selected_port: str = input()

        if (
            selected_port.isdigit()
            and int(selected_port) in self.available_com_ports.keys()
        ):
            self.selected_port = int(selected_port)
            return self.available_com_ports[self.selected_port]

        selected_port_id = self.get_port_id(selected_port)

        if selected_port_id != -1:
            self.selected_port = selected_port_id
            return self.available_com_ports[self.selected_port]

        print("Invalid port selected. Please try again.")
        raise ValueError("Invalid port selected. Please try again.")

    def get_port_id(self, name: str) -> int:
        """Get the port id from the port name."""
        if name in self.available_com_ports.values():
            return list(self.available_com_ports.keys())[
                list(self.available_com_ports.values()).index(name)
            ]

        return -1

    def has_port(self, port_name: str) -> bool:
        """Check if the port name is available."""
        return port_name in self.available_com_ports.values()

    def get_port_name(self, port_id: int) -> str:
        """Get the port name from the port id."""
        return self.available_com_ports[port_id]

    def update_available_ports(self) -> None:
        """Update the available ports."""
        com_ports = list(comports())
        self.available_com_ports = {i: port.device for i, port in enumerate(com_ports)}

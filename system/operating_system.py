"""Module to handle different operating systems."""

from enum import StrEnum
from platform import system as os


class OS(StrEnum):
    """Enum for different operating systems."""

    WINDOWS = "Windows"
    LINUX = "Linux"
    MAC = "Darwin"


class OperatingSystem:
    """Class to handle different operating systems."""

    def setup(self):
        """Setup for the operating system."""
        os_string = os()
        if os_string == OS.WINDOWS:
            self.setup_windows()
        elif os_string == OS.LINUX:
            self.setup_linux()
        elif os_string == OS.MAC:
            self.setup_mac()
        else:
            raise ValueError("Operating System not supported")

        print(f"Running on {os_string}")

    def setup_windows(self):
        """Setup for Windows operating system."""
        print("Setting up Windows operating system...")

    def setup_linux(self):
        """Setup for Linux operating system."""
        raise ValueError(f"Linux operating system, {os()}, not configured yet.")

    def setup_mac(self):
        """Setup for MacOS operating system."""
        raise ValueError(f"MacOS, {os()}, not configured yet.")

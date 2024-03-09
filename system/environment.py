"""Environment variables"""

from typing import TypeVar, Any, Final
import ujson as json
from shared_types._types import JSON
from pathlib import Path
import pathlib

ROOT_DIRECTORY: Final[Path] = pathlib.Path().resolve()


class Environment:
    """Environment variables"""

    T = TypeVar("T", JSON, str, int, float, bool, None)
    ENV_FILE_NAME = ".env"
    env_values: JSON

    @staticmethod
    def initialize():
        with open(
            f"{ROOT_DIRECTORY}/{Environment.ENV_FILE_NAME}", "r", encoding="utf-8"
        ) as json_file:
            Environment.env_values: JSON = json.load(json_file)
            print(f"Env variables: {Environment.env_values}")

    @staticmethod
    def get(key: str) -> Any:
        """Get environment variable by key."""
        return Environment.env_values[key]


Environment.initialize()
DEBUG_MODE: Final[bool] = Environment.get("debug_mode")
DEVICE_PORT: Final[str] = Environment.get("port")

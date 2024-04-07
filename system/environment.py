"""Environment variables"""

from typing import TypeVar, Any, Final, cast
import ujson as json
from shared_types._types import JSON
from pathlib import Path
import pathlib
from system.json_reader import JsonReader

ROOT_DIRECTORY: Final[Path] = pathlib.Path().resolve()


class EnvironmentVariables:
    debug_mode: bool
    port: str
    keyboard_enabled: bool
    flip_y_haply: bool


class Environment(JsonReader):
    """Environment variables"""

    ENV_FILE_NAME = ".env"
    env_variables: EnvironmentVariables = cast(EnvironmentVariables, None)

    @staticmethod
    def get() -> EnvironmentVariables:
        if not Environment.env_variables:
            Environment.env_variables = Environment.get_object(
                f"{ROOT_DIRECTORY}/{Environment.ENV_FILE_NAME}"
            )

        return Environment.env_variables

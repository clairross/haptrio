from typing import TypeVar, cast, NamedTuple
import ujson as json
from shared_types._types import JSON


class JsonReader:
    T = TypeVar("T")

    @staticmethod
    def get_object[T](file_path: str) -> T:
        with open(file_path, "r", encoding="utf-8") as json_file:
            json_data: JSON = json.load(json_file)
            data: T = cast(T, JsonReader.__to_tuple(json_data))

            return data

    @staticmethod
    def __to_tuple(parsed_dict: JSON) -> object:
        # Define a new named tuple class with the keys of json_data as field names
        NamedTupleClass = NamedTuple(
            "NamedTupleClass",
            [(key, type(value)) for key, value in parsed_dict.items()],
        )

        # Create an instance of this class with the values of json_data as field values
        dict_values = (
            JsonReader.__to_tuple(value) if isinstance(value, dict) else value
            for value in parsed_dict.values()
        )

        return NamedTupleClass(*dict_values)

from typing import TypedDict, cast
from system.json_reader import JsonReader

RESOURCES_PATH: str = "resources/resources.json"


class ImageResources(TypedDict):
    bass_clef: str
    bass_clef_staff: str
    eighth_note: str
    half_note: str
    note_inventory_background: str
    note_inventory_background_open: str
    quarter_note: str
    selection_box: str
    selection_box_hover: str
    staff: str
    treble_clef: str
    treble_clef_staff: str
    user_icon_select: str


class Resources(TypedDict):
    app_icon: str
    images: ImageResources


class ResourceManager(JsonReader):
    resources: Resources = cast(Resources, None)

    @staticmethod
    def get_resources() -> Resources:
        if not ResourceManager.resources:
            ResourceManager.resources = ResourceManager.get_object(RESOURCES_PATH)

        return ResourceManager.resources

from py5 import Py5Image as Image
from typing import cast, NamedTuple, List, TypedDict
from system.json_reader import JsonReader
from processing.sketch_manager import SketchManager


class ImageResources:
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
    xylophone: str


class SoundResources:
    error: str
    note_a: str
    note_b: str
    note_c: str
    note_d: str
    note_e: str
    note_f: str
    note_g: str
    note_c_high: str


class SongResources:
    song_notes: str


class RawSongNote(NamedTuple):
    note: str
    duration: str


class Images(NamedTuple):
    bass_clef: Image
    bass_clef_staff: Image
    eighth_note: Image
    half_note: Image
    note_inventory_background: Image
    note_inventory_background_open: Image
    quarter_note: Image
    selection_box: Image
    selection_box_hover: Image
    staff: Image
    treble_clef: Image
    treble_clef_staff: Image
    user_icon_select: Image
    xylophone: Image


class Songs:
    rain_rain_go_away: List[RawSongNote]
    when_the_saints_go_marching_in: List[RawSongNote]


class Resources:
    app_icon: str
    images: ImageResources
    sounds: SoundResources
    songs: SongResources


class ResourceManager(JsonReader):
    RESOURCES_PATH: str = "resources/resources.json"
    resources: Resources = cast(Resources, None)

    @staticmethod
    def get() -> Resources:
        if not ResourceManager.resources:
            ResourceManager.resources = ResourceManager.get_object(
                ResourceManager.RESOURCES_PATH
            )

        return ResourceManager.resources


class SongNoteParser(JsonReader):
    songs: Songs = cast(Songs, None)

    @staticmethod
    def get() -> Songs:
        if not SongNoteParser.songs:
            SongNoteParser.songs = SongNoteParser.get_object(
                ResourceManager.get().songs.song_notes
            )

        return SongNoteParser.songs


class ImageParser(JsonReader):
    images: Images = cast(Images, None)

    @staticmethod
    def get() -> Images:
        if not ImageParser.images:
            load_image = SketchManager.get_current_sketch().load_image
            image_links = ResourceManager.get().images

            ImageParser.images = Images(
                bass_clef=load_image(image_links.bass_clef, dst=cast(Image, None)),
                bass_clef_staff=load_image(
                    image_links.bass_clef_staff, dst=cast(Image, None)
                ),
                eighth_note=load_image(image_links.eighth_note, dst=cast(Image, None)),
                half_note=load_image(image_links.half_note, dst=cast(Image, None)),
                note_inventory_background=load_image(
                    image_links.note_inventory_background, dst=cast(Image, None)
                ),
                note_inventory_background_open=load_image(
                    image_links.note_inventory_background_open, dst=cast(Image, None)
                ),
                quarter_note=load_image(
                    image_links.quarter_note, dst=cast(Image, None)
                ),
                selection_box=load_image(
                    image_links.selection_box, dst=cast(Image, None)
                ),
                selection_box_hover=load_image(
                    image_links.selection_box_hover, dst=cast(Image, None)
                ),
                staff=load_image(image_links.staff, dst=cast(Image, None)),
                treble_clef=load_image(image_links.treble_clef, dst=cast(Image, None)),
                treble_clef_staff=load_image(
                    image_links.treble_clef_staff, dst=cast(Image, None)
                ),
                user_icon_select=load_image(
                    image_links.user_icon_select, dst=cast(Image, None)
                ),
                xylophone=load_image(image_links.xylophone, dst=cast(Image, None)),
            )

        return ImageParser.images

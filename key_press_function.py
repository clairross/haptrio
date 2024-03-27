from playsound import playsound
from resources.resource_manager import ResourceManager  # Adjust the import path as necessary

def setup():
    global sound_resources
    resources = ResourceManager.get_resources()
    sound_resources = resources['sounds']

def draw():
    pass

def key_pressed():
    key_to_sound = {
        'a': sound_resources['note_a'],
        'b': sound_resources['note_b'],
        'c': sound_resources['note_c'],
        'd': sound_resources['note_d'],
        'e': sound_resources['note_e'],
        'f': sound_resources['note_f'],
        'g': sound_resources['note_g'],
        'z': sound_resources['note_c_high']
    }
    sound_file = key_to_sound.get(py5.key.lower(), sound_resources['error'])
    playsound(sound_file)

py5.run_sketch()

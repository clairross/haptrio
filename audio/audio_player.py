from pygame.mixer import Sound, init


class AudioPlayer:

    def __init__(self, audio_file: str):
        init()
        self.sound = Sound(audio_file)

    def play(self):
        self.sound.play()

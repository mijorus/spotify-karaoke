import pygame
import os

class Stems():
    vocals = None
    no_vocals = None

    @staticmethod
    def play_stems(track_name: str):
        print('Playing audio...')

        Stems.vocals = pygame.mixer.Sound(os.path.join(tracks_dir, 'separated', 'htdemucs', track_name, 'vocals.mp3'))
        Stems.no_vocals = pygame.mixer.Sound(os.path.join(tracks_dir, 'separated', 'htdemucs', track_name, 'no_vocals.mp3'))

        Stems.vocals.set_volume(0.1)

        Stems.vocals.play()
        Stems.no_vocals.play()

    @staticmethod
    def stop_stems():
        if Stems.vocals:
            Stems.vocals.stop()

        if Stems.no_vocals:
            Stems.no_vocals.stop()
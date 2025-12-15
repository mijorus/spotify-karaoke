import pygame
import os

from spotify_karaoke.constants import tracks_dir, separated_tracks_subdir
from spotify_karaoke.State import State
class Stems():
    vocals = None
    no_vocals = None

    @staticmethod
    def play_stems(track_name: str):
        print('🔉 Playing audio...')

        vocals = '/'.join(['storage', 'separated', 'htdemucs', track_name, 'vocals.mp3'])
        no_vocals = '/'.join(['storage', 'separated', 'htdemucs', track_name, 'no_vocals.mp3'])

        State.update_track(vocals_track=vocals, inst_track=no_vocals)
        # Stems.vocals = pygame.mixer.Sound(os.path.join(separated_tracks_subdir, track_name, 'vocals.mp3'))
        # Stems.no_vocals = pygame.mixer.Sound(os.path.join(separated_tracks_subdir, track_name, 'no_vocals.mp3'))

        # Stems.vocals.set_volume(0.1)

        # Stems.vocals.play()
        # Stems.no_vocals.play()

    @staticmethod
    def stop_stems():
        State.update_track(vocals_track=None, inst_track=None)
        # if Stems.vocals:
        #     Stems.vocals.stop()

        # if Stems.no_vocals:
        #     Stems.no_vocals.stop()
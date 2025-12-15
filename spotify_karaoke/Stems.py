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

        vocals = '/'.join(['/storage', 'tracks', 'separated', 'htdemucs', track_name, 'vocals.mp3'])
        no_vocals = '/'.join(['/storage', 'tracks', 'separated', 'htdemucs', track_name, 'no_vocals.mp3'])
        State.update_track(vocals_track=vocals, inst_track=no_vocals)

    @staticmethod
    def stop_stems():
        State.update_track(vocals_track=None, inst_track=None)
    
    @staticmethod
    def set_progress(p):
        State.update_track_progress(p)
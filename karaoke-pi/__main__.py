import spotipy
import dotenv
from spotipy.oauth2 import SpotifyOAuth
import yt_dlp
from time import sleep
import demucs.separate
import pygame
import os
import multiprocessing
import subprocess

dotenv.load_dotenv()
pygame.mixer.init()

current_dir = os.path.dirname(os.path.abspath(__file__))
storage_dir = os.getenv('APP_STORAGE', os.path.join(current_dir, '..', 'storage'))
tracks_dir = os.path.join(storage_dir, 'tracks')
scopes = "app-remote-control,streaming,user-read-playback-state,user-modify-playback-state,user-read-currently-playing"

class SpotifyImpl():
    playback_state = None
    is_playing_track = None
    client: spotipy.Spotify = None

    @staticmethod
    def init():
        if not SpotifyImpl.client:
            SpotifyImpl.client = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scopes))

    @staticmethod
    def refresh_playback_state():
        playback_state = SpotifyImpl.client.current_playback()
        SpotifyImpl.playback_state = playback_state
        SpotifyImpl.is_playing_track = (playback_state and playback_state['is_playing'] \
                                        and playback_state['currently_playing_type'] == 'track')


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


def download_song(query):
    target_file = os.path.join(tracks_dir, f'{query}.mp3')
    if (not os.path.isfile(target_file)):
        ydl_opts = {
            'quiet': True,
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(tracks_dir, f'{query}.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print('Downloading track from yt')
            ydl.download([f'ytsearch1:"{query}"'])


    if not os.path.exists(
        os.path.join(tracks_dir, 'separated', 'htdemucs', query)
    ):
        print('Separating track')
        subprocess.run(['python3', '-m', 'demucs', "--mp3", "--two-stems", "vocals", "--shifts", "1", target_file, '--out', os.path.join(tracks_dir, 'separated')])

def load_new_track():
    isrc = SpotifyImpl.playback_state['item']['external_ids'].get('isrc')

    if not isrc:
        return

    SpotifyImpl.client.pause_playback()

    download_song(query=isrc)

    SpotifyImpl.client.seek_track(1)
    SpotifyImpl.client.start_playback()

    Stems.play_stems(track_name=isrc)

def poll_playback():
    print('Waiting for a playing track...')

    SpotifyImpl.init()

    while not SpotifyImpl.is_playing_track:
        sleep(2)
        SpotifyImpl.refresh_playback_state()

    # load_track_process = multiprocessing.Process(target=load_new_track)
    # load_track_process.start()

    isrc = SpotifyImpl.playback_state['item']['external_ids'].get('isrc')
    curr_track_id = SpotifyImpl.playback_state['item']['id']

    if not isrc:
        return

    SpotifyImpl.client.pause_playback()

    load_track_process = multiprocessing.Process(
        target=download_song,
        args=(isrc,)
    )

    load_track_process.start()

    while load_track_process.is_alive():
        sleep(2)
        SpotifyImpl.refresh_playback_state()

        if SpotifyImpl.playback_state['item']['id'] != curr_track_id:
            print('Track changed, forcing terminate old track...')
            load_track_process.kill()
            load_track_process.join()

            poll_playback()
            return
    
    SpotifyImpl.client.seek_track(1)
    SpotifyImpl.refresh_playback_state()

    if not SpotifyImpl.playback_state['is_playing']:
        SpotifyImpl.client.start_playback()

    print(f'Playing {isrc}')
    Stems.play_stems(track_name=isrc)

    SpotifyImpl.refresh_playback_state()

    while SpotifyImpl.is_playing_track:
        sleep(2)

        curr_track_id = SpotifyImpl.playback_state['item']['id']
        SpotifyImpl.refresh_playback_state()

        if SpotifyImpl.playback_state['item']['id'] != curr_track_id:
            break

    Stems.stop_stems()
    poll_playback()

def main():
    if not os.path.exists(storage_dir):
        os.mkdir(storage_dir)
    
    if not os.path.exists(tracks_dir):
        os.mkdir(tracks_dir)

    poll_playback()

if __name__ == '__main__':
    main()
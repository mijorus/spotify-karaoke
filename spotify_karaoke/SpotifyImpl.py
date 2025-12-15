import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import CacheFileHandler

from spotify_karaoke.constants import scopes, storage_dir


class SpotifyImpl():
    playback_state = None
    is_playing_track = None
    client: spotipy.Spotify = None

    @staticmethod
    def init():
        if not SpotifyImpl.client:
            cache_manager = CacheFileHandler(cache_path=os.path.join(storage_dir, '.cache'))
            auth_manager = SpotifyOAuth(scope=scopes, cache_handler=cache_manager)
            SpotifyImpl.client = spotipy.Spotify(auth_manager=auth_manager)

    @staticmethod
    def force_pause():
        try:
            SpotifyImpl.client.pause_playback()
        except:
            pass

    @staticmethod
    def refresh_playback_state():
        playback_state = SpotifyImpl.client.current_playback()
        SpotifyImpl.playback_state = playback_state
        SpotifyImpl.is_playing_track = (playback_state and playback_state['is_playing'] \
                                        # and playback_state['actions'].get('pausing', False)
                                        and playback_state['currently_playing_type'] == 'track')

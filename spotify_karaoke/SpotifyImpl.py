import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import CacheFileHandler


class SpotifyImpl():
    playback_state = None
    is_playing_track = None
    client: spotipy.Spotify = None

    @staticmethod
    def init():
        if not SpotifyImpl.client:
            SpotifyImpl.client = spotipy.Spotify(auth_manager=SpotifyOAuth(
                scope=scopes,
                cache_handler=CacheFileHandler))

    @staticmethod
    def refresh_playback_state():
        playback_state = SpotifyImpl.client.current_playback()
        SpotifyImpl.playback_state = playback_state
        SpotifyImpl.is_playing_track = (playback_state and playback_state['is_playing'] \
                                        and playback_state['currently_playing_type'] == 'track')

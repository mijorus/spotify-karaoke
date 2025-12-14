import spotipy
from spotipy.oauth2 import SpotifyOAuth

from spotify_karaoke.constants import scopes


class SpotifyImpl():
    playback_state = None
    is_playing_track = None
    client: spotipy.Spotify = None
    
    @staticmethod
    def force_pause():
        try:
            SpotifyImpl.client.pause_playback()
        except:
            pass

    @staticmethod
    def init():
        if not SpotifyImpl.client:
            SpotifyImpl.client = spotipy.Spotify(auth_manager=SpotifyOAuth(
                scope=scopes))

    @staticmethod
    def refresh_playback_state():
        playback_state = SpotifyImpl.client.current_playback()
        SpotifyImpl.playback_state = playback_state
        SpotifyImpl.is_playing_track = (playback_state and playback_state['is_playing'] \
                                        and playback_state['currently_playing_type'] == 'track')

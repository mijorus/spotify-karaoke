import threading
import time

from spotify_karaoke.constants import karaoke_playlist_id, playlist_poll_interval
from spotify_karaoke.SpotifyImpl import SpotifyImpl
from spotify_karaoke.Track import Track


class PlaylistDownloader:
    tracks = []
    downloading_isrc = None
    _lock = threading.Lock()

    @staticmethod
    def status():
        with PlaylistDownloader._lock:
            tracks = list(PlaylistDownloader.tracks)

        output = [
            {
                'isrc': t['isrc'],
                'name': t['name'],
                'downloaded': Track(t['isrc']).has_loaded_successfully(),
                'downloading': t['isrc'] == PlaylistDownloader.downloading_isrc,
            }
            for t in tracks
        ]
        
        output.reverse()
        output = sorted(output, key= lambda el: el['downloaded'])
        return output

    @staticmethod
    def _run():
        while True:
            try:
                tracks = SpotifyImpl.get_playlist_tracks(karaoke_playlist_id)

                with PlaylistDownloader._lock:
                    PlaylistDownloader.tracks = tracks

                for t in tracks:
                    track = Track(t['isrc'])
                    if track.has_loaded_successfully():
                        continue

                    PlaylistDownloader.downloading_isrc = t['isrc']
                    track.load_in_thread()

                    if track.has_loaded_successfully():
                        scale = track.estimate_key_advanced()
                        track.save_track_config(name=t['name'], scale=scale)

                    PlaylistDownloader.downloading_isrc = None
            except Exception as e:
                print(f'Playlist downloader error: {e}')
                PlaylistDownloader.downloading_isrc = None

            time.sleep(playlist_poll_interval)

    @staticmethod
    def start():
        if not karaoke_playlist_id:
            print('KARAOKE_PLAYLIST not set, background playlist downloading is disabled')
            return

        threading.Thread(target=PlaylistDownloader._run, daemon=True).start()

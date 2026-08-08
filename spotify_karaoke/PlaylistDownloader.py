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

        output = []
        for t in tracks:
            track = Track(spotify_data=t)
            output.append({
                            'isrc': track.isrc,
                            'name': track.name,
                            'downloaded': track.has_loaded_successfully(),
                            'downloading': PlaylistDownloader.downloading_isrc == track.isrc,
                            'converting': (track.has_downloaded_successfully() == True and track.has_converted_successfully() == False),
                        })
        
        output.reverse()
        output = sorted(output, key= lambda el: el['downloaded'])
        return output

    @staticmethod
    def _run():
        while True:
            try:
                playlist_tracks = SpotifyImpl.get_playlist_tracks(karaoke_playlist_id)

                with PlaylistDownloader._lock:
                    PlaylistDownloader.tracks = playlist_tracks

                for t in playlist_tracks:
                    track = Track(spotify_data=t)
                    if track.has_loaded_successfully():
                        continue

                    print('Tracks needs download ' + track.name)
                    PlaylistDownloader.downloading_isrc = t['isrc']
                    track.load_in_thread()
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

import dotenv
import os
import argparse
import essentia
from pathlib import Path

dotenv.load_dotenv()

from spotify_karaoke.SpotifyImpl import SpotifyImpl
from spotify_karaoke.Track import Track
from spotify_karaoke.PlaylistDownloader import PlaylistDownloader
from spotify_karaoke.web import server

from spotify_karaoke.constants import storage_dir, tracks_dir, scopes, separated_tracks_subdir

parser = argparse.ArgumentParser()
parser.add_argument("--refresh-scales", action="store_true", help="Set flag to True if present")
args = parser.parse_args()

def main():
    if not os.path.exists(storage_dir):
        os.mkdir(storage_dir)

    if not os.path.exists(tracks_dir):
        os.mkdir(tracks_dir)
        
    if args.refresh_scales:
        track_dir_files = os.listdir(path=tracks_dir)
        for f in track_dir_files:
            trackfile = Path(f)
            if trackfile.suffix == '.mp3':
                print(f'Refreshing {trackfile.stem}')
                track = Track(isrc=trackfile.stem)
                track_config = track.get_config()
                
                if not track_config:
                    continue
                
                new_track = Track(isrc=trackfile.stem, name=track_config['track']['name'])
                new_track.save_track_config()
        return

    SpotifyImpl.init()
    PlaylistDownloader.start()
    server.start()

if __name__ == '__main__':
    main()
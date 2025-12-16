import dotenv
import os

from spotify_karaoke.SpotifyImpl import SpotifyImpl
from spotify_karaoke.Track import Track
from spotify_karaoke.web import server

from spotify_karaoke.constants import storage_dir, tracks_dir, scopes, separated_tracks_subdir

dotenv.load_dotenv()

def main():
    if not os.path.exists(storage_dir):
        os.mkdir(storage_dir)
    
    if not os.path.exists(tracks_dir):
        os.mkdir(tracks_dir)
    
    SpotifyImpl.init()
    server.start()

if __name__ == '__main__':
    main()
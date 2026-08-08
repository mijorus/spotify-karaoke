# import dotenv
# import os

# from spotify_karaoke.SpotifyImpl import SpotifyImpl
# from spotify_karaoke.Track import Track, load_track

# from spotify_karaoke.constants import storage_dir, tracks_dir

# dotenv.load_dotenv()

# def main():
#     if not os.path.exists(storage_dir):
#         os.mkdir(storage_dir)

#     if not os.path.exists(tracks_dir):
#         os.mkdir(tracks_dir)

#     playlist_id = os.environ['KARAOKE_PLAYLIST']

#     SpotifyImpl.init()
#     tracks = SpotifyImpl.get_playlist_tracks(playlist_id)

#     print(f'Found {len(tracks)} tracks in playlist')

#     for track in tracks:
#         isrc = track['isrc']
#         name = track['name']
#         t = Track(isrc)
#         if t.has_loaded_successfully():
#             print(f'[skip] {name} ({isrc})')
#             continue
#         print(f'[load] {name} ({isrc})')
#         load_track(t.get_track_file_path(), isrc)

# if __name__ == '__main__':
#     main()

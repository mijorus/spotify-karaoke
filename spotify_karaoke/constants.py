import os

current_dir = os.path.dirname(os.path.abspath(__file__))
storage_dir = os.getenv('APP_STORAGE', os.path.join(current_dir, '..', 'storage'))
tracks_dir = os.path.join(storage_dir, 'tracks')
separated_tracks_dir = os.path.join(tracks_dir, 'separated')
separated_tracks_subdir = os.path.join(separated_tracks_dir, 'htdemucs')
scopes = "app-remote-control,streaming,user-read-playback-state,user-modify-playback-state,user-read-currently-playing"
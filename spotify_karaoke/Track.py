import os
import librosa
import torch
import configparser
import yt_dlp
import subprocess
import numpy as np
from spotify_karaoke.TUI import TUI
from spotify_karaoke.constants import tracks_dir, separated_tracks_dir, separated_tracks_subdir

class Track():
    @staticmethod
    def estimate_key_advanced(isrc):
        target_file = Track.get_track_file_path(isrc)
        # Load audio
        y, sr = librosa.load(target_file)
        
        # Compute chromagram
        chromagram = librosa.feature.chroma_cqt(y=y, sr=sr)
        
        # Average chroma features
        chroma_avg = np.mean(chromagram, axis=1)
        
        # Krumhansl-Schmuckler key profiles
        major_profile = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 
                                2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
        minor_profile = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 
                                2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
        
        # Normalize
        chroma_avg = chroma_avg / np.sum(chroma_avg)
        
        # Calculate correlation for all keys
        keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 
                'F#', 'G', 'G#', 'A', 'A#', 'B']
        
        major_correlations = []
        minor_correlations = []
        
        for i in range(12):
            # Rotate profiles to match key
            major_rotated = np.roll(major_profile, i)
            minor_rotated = np.roll(minor_profile, i)
            
            # Calculate correlation
            major_corr = np.corrcoef(chroma_avg, major_rotated)[0, 1]
            minor_corr = np.corrcoef(chroma_avg, minor_rotated)[0, 1]
            
            major_correlations.append(major_corr)
            minor_correlations.append(minor_corr)
        
        # Find best match
        max_major = max(major_correlations)
        max_minor = max(minor_correlations)
        
        if max_major > max_minor:
            key_idx = major_correlations.index(max_major)
            return f"{keys[key_idx]} major"
        else:
            key_idx = minor_correlations.index(max_minor)
            return f"{keys[key_idx]} minor"

    @staticmethod
    def get_track_file_path(isrc):
        return os.path.join(tracks_dir, f'{isrc}.mp3')
    
    @staticmethod
    def get_track_config_path(isrc):
        return os.path.join(tracks_dir, f'{isrc}.conf')

    def get_config(isrc: str):
        if not os.path.isfile(Track.get_track_config_path(isrc)):
            return None

        config = configparser.ConfigParser()
        config.read(Track.get_track_config_path(isrc))
        
        return config

    def save_track_config(isrc: str, name: str, scale: str):
        config = configparser.ConfigParser()
        
        config['track'] = {
            'isrc': isrc,
            'name': name, 
            'scale': scale
        }

        with open(os.path.join(tracks_dir, f'{isrc}.conf'), 'w+') as conf_file:
            config.write(conf_file)

    def has_loaded_successfully(isrc: str):
        return os.path.exists(Track.get_track_file_path(isrc)) and \
            os.path.exists(os.path.join(separated_tracks_subdir, isrc))

    @staticmethod
    def load(isrc):
        target_file = Track.get_track_file_path(isrc)

        if (not os.path.isfile(target_file)):
            ydl_opts = {
                # 'quiet': True,
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(tracks_dir, f'{isrc}.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                TUI.display(status='Downloading track...')
                ydl.download([f'ytsearch1:"{isrc}"'])


        if not os.path.exists(
            os.path.join(tracks_dir, 'separated', 'htdemucs', isrc)
        ) and os.path.isfile(target_file):
            TUI.display(status='Separating track...')
            device = 'cpu'
            
            if torch.backends.mps.is_available():
                device = 'mps'
            
            subprocess.run(['python3', '-m', 'demucs', "--mp3", "--two-stems", "vocals", "--shifts", "1", 
                target_file, '--out', separated_tracks_dir, '--device', device],
                # stdout=subprocess.PIPE,
                # stderr=subprocess.PIPE,
                check=True
            )

# # Usage
# key = estimate_key_advanced('song.mp3')
# print(f"Detected key: {key}")
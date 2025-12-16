import os
import librosa
import torch
import configparser
import yt_dlp
import subprocess
import multiprocessing
import numpy as np
from typing import Optional
from spotify_karaoke.constants import tracks_dir, separated_tracks_dir, separated_tracks_subdir

class Track():
    loading_process: Optional[multiprocessing.Process] = None

    def __init__(self, isrc: str):
        self.isrc = isrc

    def estimate_key_advanced(self):
        target_file = self.get_track_file_path()
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

    def get_track_file_path(self):
        return os.path.join(tracks_dir, f'{self.isrc}.mp3')
    
    def get_track_config_path(self):
        return os.path.join(tracks_dir, f'{self.isrc}.conf')
    
    def get_config(self):
        if not os.path.isfile(self.get_track_config_path()):
            return None

        config = configparser.ConfigParser()
        config.read(self.get_track_config_path())

        return config

    def save_track_config(self, name: str, scale: str):
        config = configparser.ConfigParser()
        
        config['track'] = {
            'isrc': self.isrc,
            'name': name, 
            'scale': scale
        }

        with open(os.path.join(tracks_dir, f'{self.isrc}.conf'), 'w+') as conf_file:
            config.write(conf_file)

    def has_loaded_successfully(self):
        return os.path.exists(self.get_track_file_path()) and \
            os.path.exists(os.path.join(separated_tracks_subdir, self.isrc))

    def load_in_thread(self):
        Track.loading_process = multiprocessing.Process(
            target=load_track,
            args=(self.get_track_file_path(), self.isrc,)
        )

        Track.loading_process.start()
        Track.loading_process.join()

def load_track(target_file, isrc):
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
            ydl.download([f'ytsearch1:"{isrc}"'])


    if not os.path.exists(
        os.path.join(tracks_dir, 'separated', 'htdemucs', isrc)
    ) and os.path.isfile(target_file):
        device = 'cpu'
        
        if torch.backends.mps.is_available():
            device = 'mps'
        if torch.cuda.is_available():
            device = 'cuda'
        
        subprocess.run(['python3', '-m', 'demucs', "--mp3", "--two-stems", "vocals", "--shifts", "1", 
            target_file, '--out', separated_tracks_dir, '--device', device, '--mp3-preset', '4'],
            # stdout=subprocess.PIPE,
            # stderr=subprocess.PIPE,
            check=True
        )

# # Usage
# key = estimate_key_advanced('song.mp3')
# print(f"Detected key: {key}")
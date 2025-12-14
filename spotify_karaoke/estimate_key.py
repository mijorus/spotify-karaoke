import librosa
import numpy as np

def estimate_key_advanced(audio_path):
    # Load audio
    y, sr = librosa.load(audio_path)
    
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

# Usage
key = estimate_key_advanced('song.mp3')
print(f"Detected key: {key}")
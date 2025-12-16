# Spotify Karaoke

<div align="center">
  <img src="image.png" alt="image">
</div>

## About

Spotify Karaoke is karaoke application that separates vocal tracks from music using demucs.

## Performance

This project is set-up to prefer performance over quality, of a better karaoke experience.

That's how it takes to load a song on the hardware that I have available:
- M1 Macbook (16GB)  ~50.0 s
- Windows Laptop with NVIDIA T600 GPU  ~30.0 s

Both perfectly usable if you are enjoying karaoke with your friends.

## Requirements

- Spotify Premium account
- **GPU** (recommended for best performance) - CUDA or MPS supported
- FFmpeg (installed on the system)


## Installation

1. Create a new app on the [Spotify Developer Portal](https://developer.spotify.com/)
2. Populate `.env` file
2. Create conda environment:
   ```bash
   conda create -n karaoke-venv python=3.10
   conta activate karaoke-venv
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```bash
conda activate karaoke-venv
python3 -m spotify_karaoke
```

This will:
- Prompt to login to Spotify using the official APIs to control playbac
- Start a local server at `http://127.0.0.1:8080`

### How to use it

- Open Spotify on your laptop (Web / App is the same)
- Play a song
- SpotifyKaraoke will:
    - Pause the playback
    - Download the track 
    - Separate vocals and instrument tracks
    - Resume playback
- You can now sing using the Lyrics on the Spotify App


## Performance

This project performs heavy audio processing. For optimal performance:
- A fast GPU (NVIDIA CUDA or Apple Silicon with MPS) is highly recommended
- CPU processing is supported but significantly slower
- Ensure sufficient disk space for audio files and separated tracks


## Legal

**TLDR: This may violate Spotify policies. If you work for Spotify and want to take this down, please contact me: I just wanted to play karaoke.**

This project is provided for educational purposes only. 
Users are responsible for ensuring their use complies with Spotify's Terms of Service and applicable laws. Unauthorized access to or use of Spotify's services may violate their policies.

For questions or concerns regarding this project, please contact me directly.

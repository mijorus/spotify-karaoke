import os
import time
from flask import Flask, render_template, send_from_directory

from spotify_karaoke.constants import templates_dir, storage_dir
from spotify_karaoke.SpotifyImpl import SpotifyImpl
from spotify_karaoke.Track import Track

app = Flask(__name__, template_folder=templates_dir)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/storage/<path:filename>')
def serve_storage(filename):
    print(filename)
    return send_from_directory(storage_dir, filename)
    
# @app.route('/state')
# def serve_state():
#     return send_from_directory(storage_dir, 'state.json')

@app.route('/spotify_play')
def get_spotify_play():
    try:
        SpotifyImpl.client.seek_track(0)
        SpotifyImpl.client.volume(0)
        SpotifyImpl.client.start_playback()
    except:
        pass
    return {}

@app.route('/spotify_pause')
def get_spotify_pause():
    try:
        SpotifyImpl.client.pause_playback()
    except:
        pass
    return {}

@app.route('/spotify_play_loud')
def get_spotify_play_loud():
    try:
        SpotifyImpl.client.seek_track(0)
        SpotifyImpl.client.volume(50)
        SpotifyImpl.client.start_playback()
    except:
        pass
    return {}

@app.route('/state')
def get_spotify_playback_state():
    SpotifyImpl.refresh_playback_state()

    return { 
        'data': SpotifyImpl.playback_state, 
        'is_playing': SpotifyImpl.is_playing_track 
    }

@app.route('/load_song/<path:isrc>')
def get_load_song(isrc):
    start = time.time()
    track = Track(isrc)

    if track.has_loaded_successfully():
        pass
    else:
        if Track.loading_process:
            print('Killing old process')
            Track.loading_process.kill()

        track.load_in_thread()

        if track.has_loaded_successfully():
            scale = track.estimate_key_advanced()
            curr_track_name = SpotifyImpl.playback_state['item']['name']
            track.save_track_config(name=curr_track_name, scale=scale)
        else:
            return { 'status': 'fail' }

    conf =  track.get_config()['track']
    track_name = conf.get('name')
    scale = conf.get('scale')


    vocals = '/'.join(['/storage', 'tracks', 'separated', 'htdemucs', track.isrc, 'vocals.mp3'])
    no_vocals = '/'.join(['/storage', 'tracks', 'separated', 'htdemucs', track.isrc, 'no_vocals.mp3'])
    t = time.time() - start
    return {
        'status': 'ok',
        'vocals': vocals, 
        'no_vocals': no_vocals,
        'name': track_name,
        'scale': scale,
        'infos': f'Loaded in {t:.2f}s'
    }

def start():
    app.run(debug=False, host='127.0.0.1', port=os.getenv('HTTP_PORT', 8080))

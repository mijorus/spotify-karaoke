import dotenv
import yt_dlp
from time import sleep
import pygame
import os
import multiprocessing
import threading
import json
from time import time

from spotify_karaoke.SpotifyImpl import SpotifyImpl
from spotify_karaoke.Stems import Stems
from spotify_karaoke.Track import Track
from spotify_karaoke.TUI import TUI
from spotify_karaoke.State import State
from spotify_karaoke.web import server

from spotify_karaoke.constants import storage_dir, tracks_dir, scopes, separated_tracks_subdir

dotenv.load_dotenv()
pygame.mixer.init()

def update_state_file(state):
    with open(os.path.join(storage_dir, 'state.json'), 'w+') as f:
        f.write(json.dumps(state))

def poll_playback():
    # print('Waiting for a playing track...')
    State.update_state(status='Logging in...')

    SpotifyImpl.init()

    State.update_state(status='Waiting for a playing track...')

    while not SpotifyImpl.is_playing_track:
        sleep(2)
        SpotifyImpl.refresh_playback_state()

    isrc = SpotifyImpl.playback_state['item']['external_ids'].get('isrc')
    curr_track_id = SpotifyImpl.playback_state['item']['id']
    curr_track_name = SpotifyImpl.playback_state['item']['name']
    
    if SpotifyImpl.playback_state['item']['artists']:
        curr_track_name += ' - ' + ', '.join(map(lambda el: el['name'], SpotifyImpl.playback_state['item']['artists']))

    if not isrc:
        return

    if SpotifyImpl.playback_state['is_playing']:
        SpotifyImpl.force_pause()
        
    start = time()

    if not Track.has_loaded_successfully(isrc):
        State.update_state(status='Loading track...', track_name=curr_track_name)

        load_track_process = multiprocessing.Process(
            target=Track.load,
            args=(isrc,)
        )

        load_track_process.start()

        while load_track_process.is_alive():
            sleep(2)
            SpotifyImpl.refresh_playback_state()

            if SpotifyImpl.playback_state['item']['id'] != curr_track_id:
                print('Track changed, forcing terminate old track...')
                load_track_process.kill()
                load_track_process.join()

                poll_playback()
                return
    
    SpotifyImpl.refresh_playback_state()
    if SpotifyImpl.playback_state['is_playing']:
        SpotifyImpl.force_pause()
    
    track_succesful = Track.has_loaded_successfully(isrc)
    curr_track_scale = 'Unknown'

    if track_succesful:
        if not Track.get_config(isrc):
            Track.save_track_config(
                isrc=isrc,
                name=curr_track_name,
                scale=Track.estimate_key_advanced(isrc)
            )

        if SpotifyImpl.playback_state['device']['volume_percent'] > 0:
            SpotifyImpl.client.volume(0)

    SpotifyImpl.client.seek_track(0)
    SpotifyImpl.client.start_playback()
    
    if track_succesful:
        elapsed = time() - start
        State.update_state(status=f'✅ Loaded in {elapsed:.2f}s', 
            track_name=curr_track_name,
            scale=Track.get_config(isrc)['track']['scale'])
    
        Stems.play_stems(track_name=isrc)
    else:
        State.update_state(status='Track not found - fallback')
        SpotifyImpl.client.volume(50)

    SpotifyImpl.refresh_playback_state()

    while SpotifyImpl.is_playing_track:
        sleep(2)

        curr_track_id = SpotifyImpl.playback_state['item']['id']
        SpotifyImpl.refresh_playback_state()
        
        Stems.set_progress(SpotifyImpl.playback_state['progress_ms'] / 1000)

        if SpotifyImpl.playback_state['item']['id'] != curr_track_id:
            break

    Stems.stop_stems()
    poll_playback()

def main():
    if not os.path.exists(storage_dir):
        os.mkdir(storage_dir)
    
    if not os.path.exists(tracks_dir):
        os.mkdir(tracks_dir)
    
    update_state_file(State.state)
    State.add_listener(func=TUI.display)
    State.add_listener(func=update_state_file)

    State.update_state(status='Starting...')

    TUI.start()
    poll = threading.Thread(
        target=poll_playback,
    )
    
    poll.start()
    server.start()

if __name__ == '__main__':
    main()
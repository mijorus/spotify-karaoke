import os
import multiprocessing
from textwrap import dedent

class TUI():
    k_listener = None
    
    @staticmethod
    def start():
        pass

    @staticmethod
    def _on_press(key):
        try:
            print(f"Key pressed: {key.char}")
        except AttributeError:
            print(f"Special key pressed: {key}")

    @staticmethod
    def display(status='', track_name='', scale=''):
        TUI.clear_screen()

        message = f"""
        ### Spotify Karaoke ###
        # Status: {status}
        # Track: {track_name}
        # Scale: {scale}

        """
        
        print(dedent(message))

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

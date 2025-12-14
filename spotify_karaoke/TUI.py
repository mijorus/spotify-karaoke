import os
from textwrap import dedent

class TUI():
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

import os
from textwrap import dedent

class TUI():
    k_listener = None
    
    @staticmethod
    def start():
        pass

    @staticmethod
    def display(state):
        TUI.clear_screen()

        message = f"""
        ### Spotify Karaoke ###
        # Status: {state['status']}
        # Track: {state['track_name']}
        # Scale: {state['scale']}

        """
        
        print(dedent(message))

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

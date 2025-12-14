import os
import multiprocessing
from textwrap import dedent
import pygame
import curses

class TUI():
    message = ''
    
    @staticmethod
    def bg(stdscr):
        # Clear screen
        stdscr.clear()
        stdscr.keypad(True)
        stdscr.nodelay(True)  # Make getch() blocking
        
        while True:
            # Get a single character
            stdscr.addstr(2, 0, TUI.message)
            key = stdscr.getch()
            
            # Display what was pressed
            stdscr.refresh()
            stdscr.getch()  # Wait for another keypress before exiting
    
    @staticmethod
    def start_bg():
        curses.wrapper(TUI.bg)
        
    
    @staticmethod
    def start():
        pass
        # multiprocessing.Process(target=TUI.start_bg).start()
    #    listener = pynput.keyboard.Listener(
    #         on_release=TUI._on_press).start()
        # multiprocessing.Process(target=TUI.bg).start()

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
        TUI.message = dedent(message)

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

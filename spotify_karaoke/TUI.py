import os
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
    def display(state):
        TUI.clear_screen()

        message = f"""
        ### Spotify Karaoke ###
        # Status: {state['status']}
        # Track: {state['track_name']}
        # Scale: {state['scale']}

        """
        
        print(dedent(message))
        TUI.message = dedent(message)

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

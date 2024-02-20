import pygame
import pygame_gui
from globals import *
from session import GameState

class Assistant():   

    def __init__(self, colour):
        self.colour = colour

    def on_clicked(self, session):
        if session.gamestate == GameState.RUNNING:
            print(f"on_clicked: assistant {self.colour}")
            session.selected_assistant = self


    
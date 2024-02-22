from enum import Enum
import pygame
import pygame_gui
from globals import *
from session import GameState


class Assistant():

    def __init__(self, colour, assistant_type):
        self.type = assistant_type
        self.colour = colour

    def on_clicked(self, ui_element, session):
        if session.gamestate == GameState.RUNNING:
            print(f"on_clicked: assistant {self.colour}")
            session.selected_assistant = self


    
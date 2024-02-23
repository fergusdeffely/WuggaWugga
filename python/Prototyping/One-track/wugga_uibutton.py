from enum import Enum
import pygame
import pygame_gui
from globals import *
from session import GameState


class WuggaUIButton(pygame_gui.elements.UIButton):

    def __init__(self, rect, text, manager, anchors, name):
        super().__init__(relative_rect=rect, text=text, manager=manager, anchors=anchors)
        self._name = name


    def on_clicked(self, session, ui):
        print(f"WuggaUIButton: on_clicked: ", self._name)
        if self._name == "pause_button":                
            print("pause_button: clicked")
            if session.gamestate == GameState.RUNNING:
                session.timeline.pause()
                session.gamestate = GameState.PAUSED
                self.set_text("Unpause")
            else:
                session.timeline.unpause()
                session.gamestate = GameState.RUNNING
                self.set_text("Pause")
                




    


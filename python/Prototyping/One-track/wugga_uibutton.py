from enum import Enum
import pygame
import pygame_gui
from globals import *
from session import GameState
from timeline_logger import timeline_logger


class WuggaUIButton(pygame_gui.elements.UIButton):

    def __init__(self, rect, text, manager, anchors, name):
        super().__init__(relative_rect=rect, text=text, manager=manager, anchors=anchors)
        self._name = name


    def on_clicked(self, session, ui):
        print(f"WuggaUIButton: on_clicked: ", self._name)
        if self._name == "pause_button":
            ticks = pygame.time.get_ticks()
            if session.gamestate == GameState.RUNNING:                
                session.paused_at = ticks
                timeline_logger.log(f"Timeline.pause: at:{ticks}", ticks)
                session.timeline.pause()
                ui.pause()
                session.gamestate = GameState.PAUSED
                self.set_text("Unpause")
            else:               
                gap = ticks - session.paused_at
                timeline_logger.log(f"Timeline.unpause: at:{ticks}, gap:{gap}", ticks)
                session.timeline.unpause(gap)
                ui.unpause(session, gap)
                session.gamestate = GameState.RUNNING
                self.set_text("Pause")                




    


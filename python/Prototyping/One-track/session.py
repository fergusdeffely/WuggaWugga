import pygame, sys
import pygame_gui
from enum import Enum
from globals import *


class GameState(Enum):
    RUNNING = 1
    PAUSED = 2


class Session():

    selected_assistant_groupsingle = None

    def __init__(self, timeline, timeline_logger, t0, gamestate):
        self.timeline_logger = timeline_logger
        self.timeline = timeline
        self.gamestate = gamestate
        self._t0 = t0

    def get_synchronised_t0(self, frame_ticks):        
        seconds = (int)(frame_ticks / 1000)
        return seconds * 1000 + 1000 + self._t0

    @property
    def selected_assistant(self):
        if self.selected_assistant_groupsingle is None:
            return None
        return self.selected_assistant_groupsingle.sprite
    
    @selected_assistant.setter
    def selected_assistant(self, assistant):
        print("Session: creating groupsingle for selected assistant")
        self.selected_assistant_groupsingle = pygame.sprite.GroupSingle(assistant)
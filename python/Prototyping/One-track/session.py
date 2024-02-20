import pygame, sys
import pygame_gui
from enum import Enum
from globals import *


class GameState(Enum):
    RUNNING = 1
    PAUSED = 2


class Session():

    selected_assistant = None

    def __init__(self, timeline, gamestate):
        self.timeline = timeline
        self.gamestate = gamestate


    def update(time_delta):
        self.timeline.update(pygame.time.get_ticks())

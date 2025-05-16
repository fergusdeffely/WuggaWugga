import pygame, sys
import pygame_gui
from enum import Enum
from globals import *


class Session():  

    def __init__(self, timeline, t0):
        self.timeline = timeline
        self._t0 = t0

    def unpause(self, gap):
        self.timeline.unpause(gap)
        self._t0 = (self._t0 + gap) % 500

    def get_synchronised_t0(self, frame_ticks):        
        seconds = (int)(frame_ticks / 1000)
        return seconds * 1000 + 1000 + self._t0
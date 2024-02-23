from enum import Enum
import pygame
import pygame_gui
from globals import *
from session import GameState


class Assistant():

    def __init__(self, assistant_type, colour, shadow_colour):
        self.type = assistant_type
        self.emitter_type = EmitterType(self.type.value)
        self.colour = colour
        self.shadow_colour = shadow_colour

        # build the shape
        if self.type in (AssistantType.KICK_EMITTER, 
                         AssistantType.BASS_EMITTER):
            self.shape = [(0,0)]


    def __repr__(self):
        return "Assistant({}, {}, {}, {}, {})".format(self.type, 
                                                      self.emitter_type, 
                                                      self.colour, 
                                                      self.shadow_colour, 
                                                      self.shape)


    def has_location(self, location):
        return False

    
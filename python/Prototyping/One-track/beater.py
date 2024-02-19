import pygame
from enum import Enum
from globals import *


class BeaterType(Enum):
    KICK = 1
    BASS = 2


class Beater(pygame.sprite.Sprite):
    def __init__(self, location, colour, beater_type):
        super().__init__()

        self._type = beater_type
        self.location = location
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(colour)
        position = grid_to_screen(location)
        self.rect = pygame.Rect(x(position), y(position), TILE_SIZE, TILE_SIZE)


    def play(self, audio):
        if self._type == BeaterType.KICK:
            audio.play_beat()
        elif self._type == BeaterType.BASS:
            audio.play_bass()


    def update(self):
        pass
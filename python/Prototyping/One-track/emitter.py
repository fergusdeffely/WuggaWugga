import pygame
from enum import Enum
from globals import *


class Emitter(pygame.sprite.Sprite):
    def __init__(self, emitter_type, location, colour):
        super().__init__()

        self._type = emitter_type
        self.location = location
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(colour)
        position = grid_to_screen(location)
        self.rect = pygame.Rect(x(position), y(position), TILE_SIZE, TILE_SIZE)


    def play(self, audio):
        if self._type == EmitterType.KICK:
            audio.play_beat()
        elif self._type == EmitterType.BASS:
            audio.play_bass()


    def update(self):
        pass
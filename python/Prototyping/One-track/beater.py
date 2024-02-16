import pygame
from enum import Enum
from globals import *
 
class BeaterType(Enum):
    KICK = 1
    BASS = 2


class Beater(pygame.sprite.Sprite):
    def __init__(self, location, colour, beater_type):
        super().__init__()

        self.type = beater_type
        self.location = location
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))    
        self.image.fill(colour)
        position = grid_to_screen(location)
        self.rect = pygame.Rect(position[0], position[1], TILE_SIZE, TILE_SIZE)


    def get_sound(self):
        return self.sound


    def play(self, audio):
        if self.type == BeaterType.KICK:
            audio.play_beat()
        elif self.type == BeaterType.BASS:
            audio.play_bass()


    def update(self):
        # TODO add highlighting here
        pass
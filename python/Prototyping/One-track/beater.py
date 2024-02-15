import pygame
from globals import *
 
class Beater(pygame.sprite.Sprite):
    def __init__(self, location):
        super().__init__()

        self.location = location
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))    
        self.image.fill("red")
        position = grid_to_screen(location)
        self.rect = pygame.Rect(position[0], position[1], TILE_SIZE, TILE_SIZE)


    def update(self):
        # TODO add highlighting here
        pass
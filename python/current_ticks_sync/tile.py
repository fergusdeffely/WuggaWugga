import pygame
from globals import *
 
class Tile(pygame.sprite.Sprite):

    def __init__(self, location, position):
        super().__init__()

        self.location = location
        self.position = position
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))    
        self.image.fill("grey")        
        self.rect = pygame.Rect(position[0], position[1], TILE_SIZE, TILE_SIZE)
    
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)

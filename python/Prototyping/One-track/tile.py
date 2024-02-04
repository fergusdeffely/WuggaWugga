import pygame
from globals import *

class Tile(pygame.sprite.Sprite):
  def __init__(self, location):
    super().__init__()
    
    self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
    self.image.fill("grey")
    self.rect = self.image.get_rect()
    position = grid_to_screen(location)
    self.rect.x = position[0]
    self.rect.y = position[1]
    
  def update(self):
    # TODO add highlighting here
    pass
    
  def get_centre(self):
    return self.rect.center
import pygame
from globals import *
 
class Tile(pygame.sprite.Sprite):
  def __init__(self, location):
    super().__init__()

    self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))    
    self.image.fill("grey")
    position = grid_to_screen(location)
    self.rect = pygame.Rect(position[0], position[1], TILE_SIZE, TILE_SIZE)
    
    
  def update(self):
    # TODO add highlighting here
    pass
    
  def get_centre(self):
    return self.rect.center
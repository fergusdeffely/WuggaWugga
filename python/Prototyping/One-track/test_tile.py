import pygame
from globals import *

RETICULE_CORNER_SIZE = 10
RETICULE_CORNER = (RETICULE_CORNER_SIZE, RETICULE_CORNER_SIZE)

class TestTile(pygame.sprite.Sprite):
  def __init__(self, location):
    super().__init__()
    
    self.image = pygame.Surface((TILE_SIZE, TILE_SIZE)) 

    # draw the reticule
    topleft = pygame.Rect((0,0), RETICULE_CORNER)
    pygame.draw.rect(self.image, "green", topleft)
    topright = pygame.Rect((TILE_SIZE - RETICULE_CORNER_SIZE,0), RETICULE_CORNER)
    pygame.draw.rect(self.image, "green", topright)
    bottomleft = pygame.Rect((0,TILE_SIZE - RETICULE_CORNER_SIZE), RETICULE_CORNER)
    pygame.draw.rect(self.image, "green", bottomleft)
    bottomright = pygame.Rect((TILE_SIZE - RETICULE_CORNER_SIZE, TILE_SIZE - RETICULE_CORNER_SIZE), RETICULE_CORNER)
    pygame.draw.rect(self.image, "green", bottomright)

    position = grid_to_screen  
 
    position = grid_to_screen(location)
    self.rect = pygame.Rect(position[0], position[1], TILE_SIZE, TILE_SIZE)
    
  def update(self):
    # TODO add highlighting here
    pass
    
  def get_centre(self):
    return self.rect.center
import pygame
from globals import *

class Mouse(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    
    self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
    self.image.fill("blue")
    self.rect = self.image.get_rect()
    
    
  def update(self):
    position = pygame.mouse.get_pos()
    grid = get_containing_grid(position)
    
    self.rect.x = x(grid)
    self.rect.y = y(grid)
    
  
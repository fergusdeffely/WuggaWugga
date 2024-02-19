import pygame
from globals import *

class Mouse(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    
    self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA, 32)
    self.image = self.image.convert_alpha()
    self.rect = self.image.get_rect()

    frame = pygame.Rect((0,0), (TILE_SIZE, TILE_SIZE))
    pygame.draw.rect(self.image, "green", frame, 3, border_radius=3)

    
  def update(self):
    position = pygame.mouse.get_pos()
    grid = get_containing_grid(position)
    
    self.rect.x = x(grid)
    self.rect.y = y(grid)
    
  
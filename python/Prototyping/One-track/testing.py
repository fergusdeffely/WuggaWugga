import pygame, sys
from globals import *
from tile import Tile
from test_tile import TestTile
from level_data import level_map
from level import Level

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
#pygame.time.set_timer(SPAWN_TIMER_EVENT, 1000)

test_tile = TestTile((5,5))

tiles = pygame.sprite.Group()
tiles.add(test_tile)

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    elif event.type == SPAWN_TIMER_EVENT:
      pass
      
  screen.fill("black")
  
  tiles.draw(screen)

  pygame.display.update()
  clock.tick(60)

pygame.quit()

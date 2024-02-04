import pygame, sys
from globals import *
from tile import Tile
from level_data import level_map
from level import Level

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
level = Level(level_map, screen)
pygame.time.set_timer(SPAWN_TIMER_EVENT, 1000)

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    elif event.type == SPAWN_TIMER_EVENT:
      level.spawn_beatbug()
      
  screen.fill("black")
  
  level.draw()

  pygame.display.update()
  clock.tick(60)

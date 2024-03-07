import pygame, sys
from globals import *
from tile import Tile
from test_tile import TestTile
from level_data import level_map
from level import Level
from audio import Audio

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH_PIXELS, SCREEN_HEIGHT_PIXELS))
clock = pygame.time.Clock()
audio = Audio()

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    if event.type == pygame.MOUSEBUTTONUP:
      print("Mouse button clicked")
      audio.play_bass()
      pygame.time.delay(50)
      audio.play_beat()
      
  screen.fill("black")
  
  pygame.display.update()
  clock.tick(60)

pygame.quit()

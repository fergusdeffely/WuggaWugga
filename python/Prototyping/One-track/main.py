import pygame, sys
from globals import *
from tile import Tile
from level_data import level_map
from level import Level
from audio import Audio

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
audio = Audio()
level = Level(level_map, screen, audio)
pygame.time.set_timer(SPAWN_TIMER_EVENT, SPAWN_TIMER_DURATION)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == SPAWN_TIMER_EVENT:
            level.spawn_beatbug()
        elif event.type == pygame.MOUSEBUTTONUP:
            print(f"Event: MouseButtonUp : {event.button} at {screen_to_grid(event.pos)}")
            if event.button == 1:
                level.handle_click(event)
      
    screen.fill("black")
    
    level.draw()

    pygame.display.update()
    clock.tick(60)
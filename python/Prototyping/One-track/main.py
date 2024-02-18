import pygame, sys
from globals import *

from timeline import Timeline
from timeline_event import TimelineEvent
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

timeline = Timeline()
spawn_beatbug_event = TimelineEvent(pygame.time.get_ticks(), level.spawn_beatbug, 0, 2000)
timeline.add_event(spawn_beatbug_event)
paused = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            print(f"Event: MouseButtonUp : {event.button} at {screen_to_grid(event.pos)}")
            if event.button == 1:
                level.handle_click(event)
        elif event.type == PAUSE_BUTTON_CLICKED:
            print ("Event: PauseButtonClicked :")
            if level.get_paused() == False:
                timeline.pause()
                level.pause()
            else:
                timeline.unpause()
                level.unpause()
      
    screen.fill("black")

    timeline.update(pygame.time.get_ticks())
    
    level.draw()

    pygame.display.update()
    clock.tick(60)
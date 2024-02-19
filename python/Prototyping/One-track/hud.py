import pygame
from palette import Palette
from button import Button
from globals import *

class HUD():

    def __init__(self):
        # create the palette
        self.palette = Palette()

        pos = grid_to_screen((4, 1))
        self._button = Button(x(pos), y(pos), TILE_SIZE * 3, TILE_SIZE, 'Pause', self.on_pause)


    def on_pause(self):
        ui_event = pygame.event.Event(PAUSE_BUTTON_CLICKED, {})
        pygame.event.post(ui_event)


    def draw(self, surface):
        self._button.draw(surface)
        self.palette.draw(surface)


    def update(self):
        #TODO update status of palette options based on availability
        pass
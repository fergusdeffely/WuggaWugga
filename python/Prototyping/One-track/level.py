import pygame
from globals import *
from tracktile import TrackTile
from beatbug import BeatBug
from beater import Beater
from beater import BeaterType
from hud import HUD
from palette import Palette
from mouse import Mouse

class Level:

    def __init__(self, data, surface, audio):
        self._paused = False
        self._surface = surface
        self._audio = audio
        self._data = data
        self._initialise(data)

      
    def _initialise(self, data):
        # add the tiles
        self._tiles = pygame.sprite.Group()
        for y, row in enumerate(data):
            for x, cell in enumerate(row):
                if cell in ['N', 'S', 'W', 'E']:
                    tile = TrackTile((x, y), cell)
                    self._tiles.add(tile)
                elif cell == 'B':
                    # Begin
                    self._spawner_location = (x, y)
                elif cell == 'F':
                    # Finish
                    self.finish_location = (x, y)
              
        # create groups for the sprites
        self._bugs = pygame.sprite.Group()
        self._beaters = pygame.sprite.Group()

        # create the hud
        self._hud = HUD()

        # create the mouse
        self._mouse = pygame.sprite.GroupSingle(Mouse())


    def pause(self):
        self._paused = True


    def unpause(self):
        self._paused = False


    def get_paused(self):
        return self._paused


    def draw(self):
        if self._paused == False:
            self._tiles.update()
        self._tiles.draw(self._surface)

        if self._paused == False:
            self._beaters.update()
        self._beaters.draw(self._surface)

        if self._paused == False:
            self._bugs.update(self._data, self._beaters, self._audio)
        self._bugs.draw(self._surface)

        self._hud.update()
        self._hud.draw(self._surface)

        self._mouse.update()
        self._mouse.draw(self._surface)
      

    def handle_click(self, event):

        location = screen_to_grid(event.pos)

        if self._paused == True:
            return

        # check for palette option clicked
        new_colour = self._hud.palette.handle_click(location=location)
        if new_colour is not None:
            self._hud.palette.select([location, new_colour])

        # check for add beater
        cell = self._data[y(location)][x(location)]

        if(cell in "NSEW"):
            #TODO: Check if beater already exists in this location
            beater_type = None
            if self._hud.palette.selected_colour() == "red":
                beater_type = BeaterType.KICK
            elif self._hud.palette.selected_colour() == "yellow":
                beater_type = BeaterType.BASS
            
            if beater_type is not None:
                beater = Beater(location, self._hud.palette.selected_colour(), beater_type)
                self._beaters.add(beater)

    
    def spawn_beatbug(self):
        if(self._spawner_location):
            bug = BeatBug(self._spawner_location)
            self._bugs.add(bug)
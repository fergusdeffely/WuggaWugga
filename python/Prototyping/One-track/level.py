import pygame
from globals import *
from session import GameState
from tracktile import TrackTile
from beatbug import BeatBug
from beater import Beater
from beater import BeaterType
from mouse import Mouse

class Level:

    def __init__(self, data, out):
        self._out = out
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


    def update(self, gamestate, audio):
        if gamestate == GameState.RUNNING:
            self._tiles.update()
            self._beaters.update()
            self._bugs.update(self._data, self._beaters, audio)


    def draw(self, surface):
        self._tiles.draw(surface)
        self._beaters.draw(surface)
        self._bugs.draw(surface)


    def handle_click(self, position, assistant):

        location = screen_to_grid(position)

        # check if the location is valid for placement
        cell = self._data[y(location)][x(location)]

        if(cell in "NSEW"):
            #TODO: Check if beater already exists in this location
            beater_type = None
            if assistant.colour == "red":
                beater_type = BeaterType.KICK
            elif assistant.colour == "yellow":
                beater_type = BeaterType.BASS
            
            if beater_type is not None:
                beater = Beater(location, assistant.colour, beater_type)
                self._beaters.add(beater)

    
    def spawn_beatbug(self):
        if(self._spawner_location):
            bug = BeatBug(self._spawner_location)
            self._bugs.add(bug)
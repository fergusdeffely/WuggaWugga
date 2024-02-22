import pygame
from globals import *
from session import GameState
from tracktile import TrackTile
from beatbug import BeatBug
from emitter import Emitter
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
        self._emitters = pygame.sprite.Group()


    def update(self, gamestate, audio):
        if gamestate == GameState.RUNNING:
            self._tiles.update()
            self._emitters.update()
            self._bugs.update(self._data, self._emitters, audio)


    def draw(self, surface):
        self._tiles.draw(surface)
        self._emitters.draw(surface)
        self._bugs.draw(surface)


    def handle_click(self, position, assistant):

        if assistant == None:
            return

        location = screen_to_grid(position)

        # don't place over another emitter
        for emitter in self._emitters:
            if emitter.location == location:
                return

        # check if the location is valid for placement
        cell = self._data[y(location)][x(location)]

        if(cell in "NSEW"):
            #TODO: Check if emitter already exists in this location
            emitter_type = None
            if assistant.colour == "red":
                emitter_type = EmitterType.KICK
            elif assistant.colour == "yellow":
                emitter_type = EmitterType.BASS
            
            if emitter_type is not None:
                emitter = Emitter(location, assistant.colour, emitter_type)
                self._emitters.add(emitter)

    
    def spawn_beatbug(self):
        if(self._spawner_location):
            bug = BeatBug(self._spawner_location)
            self._bugs.add(bug)
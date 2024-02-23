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
        self._assistants = []

      
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

        print("level.handle_click: selected_assistant = ", assistant)

        if self.is_assistant_placeable(location, assistant):
            # add a new assistant to the level
            self._assistants.append(assistant)

            emitter = Emitter(assistant.emitter_type, location, assistant.colour)
            self._emitters.add(emitter)


    def assistant_at(self, location):
        for assistant in self._assistants:
            if assistant.has_location(location):
                return True

        return False

    def track_tile_at(self, location):
        # check if the location is valid for placement
        cell = self._data[y(location)][x(location)]

        if(cell in "NSEW"):        
            return True
        else:
            return False


    def is_assistant_placeable(self, location, assistant):
        if self.assistant_at(location):
            return False

        if self.track_tile_at(location):
            return True

        return False        
    
    def spawn_beatbug(self):
        if(self._spawner_location):
            bug = BeatBug(self._spawner_location)
            self._bugs.add(bug)

    def contains_emitter(self, location):
        return False
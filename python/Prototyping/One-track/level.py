import pygame
import copy
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
        self._tiles = pygame.sprite.Group()
        self._assistants = pygame.sprite.Group()
        self._initialise(data)

    def _initialise(self, data):
        # add the tiles        
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
        self._assistants.draw(surface)
        self._emitters.draw(surface)
        self._bugs.draw(surface)


    def handle_click(self, position, session):

        if session.selected_assistant == None:
            return

        location = screen_to_grid(position)

        if self.is_assistant_placeable(location, session.selected_assistant):
            assistant = copy.deepcopy(session.selected_assistant)
            assistant.location = location
            # create an emitter
            emitter = Emitter(assistant.emitter_type, location, 
                              assistant.colour)
            emitter.assistant = assistant

            # add a new assistant to the level
            self._assistants.add(assistant)
            self._emitters.add(emitter)

            session.selected_assistant_groupsingle = None


    def assistant_at(self, location):
        for assistant in self._assistants.sprites():
            if assistant.has_segment(location):
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

        count = 0
        for location in assistant.get_segment_locations():
            if self.track_tile_at(location):
                count += 1

        if count == 1:
            return True

        return False

    
    def spawn_beatbug(self):
        if(self._spawner_location):
            bug = BeatBug(self._spawner_location)
            self._bugs.add(bug)

    def contains_emitter(self, location):
        return False
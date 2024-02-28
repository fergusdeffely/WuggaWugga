import pygame
import copy
from globals import *
from timeline_logger import timeline_logger
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
        self._paused = False

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


    def update(self, frame_ticks, audio):
        if self._paused == False:
            self._tiles.update()
            # emitters need to know where bugs are and bugs need
            # to know where emitters are            
            self._emitters.update(frame_ticks, self._bugs, audio)
            self._bugs.update(frame_ticks, self._data, self._emitters, audio)


    def draw(self, surface):
        if DRAW_GRID == True:
            self.draw_grid(surface)
        self._tiles.draw(surface)
        self._assistants.draw(surface)
        self._emitters.draw(surface)
        self._bugs.draw(surface)


    def pause(self):
        self._paused = True


    def unpause(self, gap):
        self._paused = False
        for bug in self._bugs:
            bug.adjust_for_pause(gap)


    def draw_grid(self, surface):
        width_in_tiles = len(self._data[0])
        height_in_tiles = len(self._data)

        # vertical lines
        for x in range(width_in_tiles):
            pygame.draw.line(surface, "#75757575", (x*TILE_SIZE, 0), (x*TILE_SIZE, height_in_tiles * TILE_SIZE))

        # horiztonal lines
        for y in range(height_in_tiles):
            pygame.draw.line(surface, "#75757575", (0, y*TILE_SIZE), (width_in_tiles * TILE_SIZE, y*TILE_SIZE))


    def handle_click(self, frame_ticks, position, session):

        if session.selected_assistant == None:
            return

        location = screen_to_grid(position)

        if self.is_assistant_placeable(location, session.selected_assistant):
            assistant = copy.deepcopy(session.selected_assistant)
            assistant.location = location
            # create an emitter
            t0 = session.get_synchronised_t0(frame_ticks)            
            emitter = Emitter(t0, assistant.emitter_type, location, assistant.colour)            
            emitter.assistant = assistant
            timeline_logger.log(f"level: create em{emitter.id} at:{emitter.rect.center} t0:{t0}", frame_ticks)

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


    def spawn_beatbug(self, due_ticks, frame_ticks):
        if(self._spawner_location):
            bug = BeatBug(self._spawner_location, due_ticks)
            timeline_logger.log(f"bug{bug.id}:spawned, t0:{bug.t0}", frame_ticks)
            self._bugs.add(bug)
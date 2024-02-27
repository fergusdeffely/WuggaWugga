from enum import Enum
import pygame
import pygame_gui
from globals import *
from session import GameState


class Assistant(pygame.sprite.Sprite):

    def __init__(self, assistant_type, position, colour, shadow_colour):
        super().__init__()

        self.type = assistant_type
        self.emitter_type = EmitterType(self.type.value)
        self.colour = colour
        self.shadow_colour = shadow_colour
        # location will be set after the assistant is placed
        self.location = None

        # build the shape
        # segment format:
        # (x_off, y_off) - from root segment; defined in grid coords
        # (exit north, exit south, exit east, exit west) - path definition
        if self.type == AssistantType.KICK_EMITTER:
            self.segments = [(0,0)]
            self.exits = [(0,0,0,0)]
        if self.type == AssistantType.BASS_EMITTER:
            self.segments = [(0,0), (0, 1), (0,-1)]
            self.exits = [(1,1,0,0), (1,0,0,0), (0,1,0,0)]

        extents = self.get_segment_extents()

        width = (extents["max_plus_x"] - extents["max_minus_x"]) * TILE_SIZE + TILE_SIZE
        height = (extents["max_plus_y"] - extents["max_minus_y"]) * TILE_SIZE + TILE_SIZE

        '''
        Take the case where we have an assistant that looks like the following:
               O
               O
               OOXOO
                   O
                   O
        It will be convenient when rotating to have the root segment in the centre -
        that is at X - and to have the other segments defined in relative terms.

        To facilitate drawing, we keep an offset to the root in grid.
        In the example above the root offset would be (2,2)
        '''
        self.root_offset = (0 - extents["max_minus_x"], 0 - extents["max_minus_y"])

        self.image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.update(position)

        self.redraw(self.shadow_colour)


    def get_root_location(self):
        location = screen_to_grid(self.rect.topleft)
        root_location = (x(location) + x(self.root_offset), y(location) + y(self.root_offset))
        log(4, "Assistant.get_root_location: location (rect) = {}, root_location = {}".format(location, root_location))
        return root_location


    def get_segment_locations(self):
        segment_locations = []
        root_location = self.get_root_location()
        for segment_offset in self.segments:
            segment_locations.append((x(root_location) + x(segment_offset), 
                                      y(root_location) + y(segment_offset)))

        log(4, f"Assistant.get_segment_locations: returning: {segment_locations}")
        return segment_locations


    def get_segment_extents(self):
        max_plus_x = 0
        max_minus_x = 0
        max_plus_y = 0
        max_minus_y = 0        
        
        for segment in self.segments:
            if segment[0] > max_plus_x:
                max_plus_x = segment[0]
            if segment[0] < max_minus_x:
                max_minus_x = segment[0]
            if segment[1] > max_plus_y:
                max_plus_y = segment[1]
            if segment[1] < max_minus_y:
                max_minus_y = segment[1]

        return {"max_plus_x": max_plus_x, 
                "max_minus_x": max_minus_x, 
                "max_plus_y": max_plus_y, 
                "max_minus_y": max_minus_y}


    def get_exits(self, position):
        requested_location = screen_to_grid(position)
        # print("get_exits: seeking position = {} (location:{})".format(position, requested_location))
        # print("get_exits: assistant root location = ", self.location)

        # which segment is the requested location in?
        for i, offset in enumerate(self.segments):
            if (x(self.location) + x(offset), y(self.location) + y(offset)) == requested_location:
                return self.exits[i]
            
        return (0,0,0,0)

        
    def update(self, position):
        self.rect.x = x(position) - x(self.root_offset) * TILE_SIZE
        self.rect.y = y(position) - y(self.root_offset) * TILE_SIZE


    def redraw(self, colour):
        for segment in self.segments:
            rect = pygame.Rect((x(segment) + x(self.root_offset)) * TILE_SIZE,
                               (y(segment) + y(self.root_offset)) * TILE_SIZE,
                               TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(self.image, colour, rect, border_radius=3)


    def has_segment(self, location):
        for segment_location in self.get_segment_locations():
            if location == segment_location:
                return True

        return False                 
                                                                                                                                      

    def __repr__(self):
        repr = "Assistant(type={}\n    emitter_type={}\n".format(self.type, self.emitter_type)
        repr = repr + "    colour={}\n    shadow_colour={}\n".format(self.colour, self.shadow_colour)
        repr = repr + "    segments={}\n    root_offset={})".format(self.segments,self.root_offset)

        return repr    


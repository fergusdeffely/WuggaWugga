import time
import math
import copy
from enum import Enum
import pygame
import pygame_gui
from pygame_gui.elements import UIButton

import globals as g


class RisingFloodTransitionState(Enum):
    RISING = 0
    COMPLETE = 1


class FloodTile():
    def __init__(self, x, y, flood_level, flood_stage=None):
        self.x = x
        self.y = y
        self.location = (x, y)
        self.flood_level = flood_level
        self.flood_stage = flood_stage
        self.surface = None


class RisingFloodTransition():
    def __init__(self, surface, peaks, num_h_tiles, num_v_tiles):
        self._transitionState = RisingFloodTransitionState.RISING
        self._throttle = 0

        self._peak_locations = peaks
        self._surface = surface
        self._surface_stage_1 = g.greyscale(surface)

        self._num_h_tiles = num_h_tiles
        self._num_v_tiles = num_v_tiles
        
        self._tile_width = int(surface.width / num_h_tiles)
        self._tile_height = int(surface.height / num_v_tiles)

        # for larger resolutions of flood tiles, 
        # we need to pad out tiles to the right and bottom
        #
        # e.g. 100x50
        #      tile_width = 1024 / 100 = 10
        #      tile_width * num_h_tiles = 1000 
        #      ... leaves two full tiles and one partial tile missing on the right hand side

        rightmost = self._tile_width * num_h_tiles
        while rightmost < surface.width:
            self._num_h_tiles += 1
            rightmost = self._tile_width * self._num_h_tiles
        bottommost = self._tile_height * num_v_tiles
        while bottommost < surface.height:
            self._num_v_tiles += 1
            bottommost = self._tile_height * self._num_v_tiles

        self._tiles = {}
                
        for y in range(self._num_v_tiles):
            for x in range(self._num_h_tiles):
                # zero initial level for all tiles
                self._tiles[(x,y)] = FloodTile(x, y, 0)

        self._stage_1_flood_level = self._hillify()


    @property
    def complete(self):
        return self._transitionState == RisingFloodTransitionState.COMPLETE


    def _hillify(self):
        # assumes peak locations have been initialised

        # starts at peak level (max) and assigns a level of one lower
        # to all neighbours (that don't already have a level)
        # repeats this process for the next level until all tiles are
        # processed

        # start at the top
        current_low_tiles = []
        lowest_flood_level = g.MAX_FLOOD_LEVEL
        
        # begin by updating the level of tiles at the peak locations
        for location in self._peak_locations:
            peak_tile = self._tiles[location]
            peak_tile.flood_level = g.MAX_FLOOD_LEVEL
            current_low_tiles.append(peak_tile)
        
        num_processed = len(current_low_tiles)
        
        while num_processed < self._num_v_tiles * self._num_h_tiles:            
            current_low_tiles = self._go_downhill(current_low_tiles)
            num_processed += len(current_low_tiles)            
            # the last flood level stored (lowest) will be the first processed by update
            lowest_flood_level -= 1

        return lowest_flood_level


    def _find_neighbours(self, location):

        # generate a list of neighbouring tile locations

        # 4 2 5
        # 0 T 1
        # 6 3 7

        neighbours = []
        x = location[0]
        y = location[1]
        left  = x - 1
        right = x + 1
        up    = y - 1
        down =  y + 1

        # add orthogonally adjacent tiles first - it helps in various
        # situations to process these first

        if left >= 0:
            neighbours.append((left, y))
        if right < self._num_h_tiles:
            neighbours.append((right, y))
        if up >= 0:
            neighbours.append((x, up))
        if down < self._num_v_tiles:
            neighbours.append((x, down))

        # diagonally adjacent tiles
        if left >= 0 and up >= 0:
            neighbours.append((left, up))
        if left >= 0 and down < self._num_v_tiles:
            neighbours.append((left, down))
        if right < self._num_h_tiles and up >= 0:
            neighbours.append((right, up))
        if right < self._num_h_tiles and down < self._num_v_tiles:
            neighbours.append((right, down))

        return neighbours


    def _go_downhill(self, tiles):

        processed_tiles = []

        for tile in tiles:

            neighbour_locations = self._find_neighbours(tile.location)

            for neighbour_location in neighbour_locations:
                neighbour_tile = self._tiles[neighbour_location]
                if neighbour_tile.flood_level == 0:
                    neighbour_tile.flood_level = tile.flood_level - 1
                    processed_tiles.append(neighbour_tile)

        return processed_tiles


    def update(self):
        # just skip if everything is already flooded
        if self._stage_1_flood_level > g.MAX_FLOOD_LEVEL:
            self._transitionState = RisingFloodTransitionState.COMPLETE
            return

        # only process every five frames
        self._throttle += 1
        if self._throttle % 5 != 0:
            return

        flood_level_tiles = [tile for tile in self._tiles.values() if tile.flood_level == self._stage_1_flood_level]

        for tile in flood_level_tiles:
            tile.flood_stage = 1

        self._stage_1_flood_level += 1


    def draw(self, surface):
        surface.blit(self._surface, self._surface.get_rect())

        stage_1_tiles = [tile for tile in self._tiles.values() if tile.flood_stage == 1]

        for tile in stage_1_tiles:
            rect = pygame.Rect(tile.x * self._tile_width, 
                               tile.y * self._tile_height, 
                               self._tile_width, 
                               self._tile_height)
                               
            surface_rect = self._surface.get_rect()

            # clip border tiles to be contained in screen surface
            if rect.bottom > surface_rect.bottom:
                rect.bottom = surface_rect.bottom
            if rect.right > surface_rect.right:
                rect.right = surface_rect.right

            surface.blit(self._surface_stage_1, dest=rect, area=rect)


    def _log_tile_levels(self):
        g.log(3, "Rising Flood Transition - current tile map")
        row = ""
        for y in range(self._num_v_tiles):
            for x in range(self._num_h_tiles):
                row += f"{self._tiles[(x, y)].flood_level:3}"
            
            g.log(3, row)
            g.log(2,"")
            row = ""
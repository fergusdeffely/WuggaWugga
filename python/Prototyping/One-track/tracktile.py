import pygame
from globals import *
from tile import Tile

class TrackTile(Tile):

    def __init__(self, location, whereto):
        super().__init__(location)
        self.whereto = whereto


    def get_centre():
        # centre in screen coords
        print ("TrackTile.get_centre()", self.location)
        x = self.location[0] * TILE_SIZE + TILE_SIZE / 2
        y = self.location[1] * TILE_SIZE + TILE_SIZE / 2
        return ((x, y))
    
      
    def past_centre(self, compare_position):
        centre = self.get_centre()
        
        if self.whereto == 'N':
            if compare_position[1] <= centre[1]:
                return true
            else:
                return false
        elif self.whereto == 'S':
            if compare_position[1] >= centre[1]:
                return true
            else:
                return false
        elif self.whereto == 'W':
            if compare_position[0] <= centre[0]:
                return true
            else:
                return false    
        elif self.whereto == 'S':
            if compare_position[0] >= centre[0]:
                return true
            else:
                return false
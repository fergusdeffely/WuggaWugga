import pygame
from globals import *
from tile import Tile

class TrackTile(Tile):

    def __init__(self, location, position, exits, info):
        super().__init__(location, position)
        self.exits = exits
        self.info = info

    def __repr__(self):
        return f"TrackTile: rect: {self.rect} exits:{self.exits} info:{self.info}"
